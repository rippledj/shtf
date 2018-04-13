# shtf.py
# This app scrapes the daily stock data from the front page of finviz.com
# The app needs to be scheduled to run after the stock market closes each day (~9pm EST)
# The app then collects the financial data from each stocks homepage at finviz.com
# The app also tracks the stocks for 10 days and records daily price closes
# The data is entered into a MySQL database for later analysis
#
#
# Author: Joseph Lee
# Date: April 2017

#import libraries
import logging
import datetime
import csv
import urllib
from bs4 import BeautifulSoup
import urllib2
import MySQLdb
import time
import decimal
import sys
import os
import string

# Function to strip strings
#
#
def strip_list(the_list):
	return [line.strip() for line in the_list]


# Setup logging
def setup_logger(log_file):
    logger = logging.getLogger('SHTF_stock_screener')
    log_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)


# Previous days screener function
def process_previous_days_new_close(url, database_array, insert_mode):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	# Print message to stdout and log
	print "Collecting previous day data from database..."
	logger.info("Collecting previous day data from database: " + datetime.datetime.today().strftime('%Y-%m-%d'))
	# Collect previous day stocks that need data and put into list of primary key id and ticker
	previous_day_array = collect_previous_day_tickers(database_array)

	# If no errors or no data to update
	if previous_day_array:
		# Print message to stdout and log
		print "Collecting price data for previous day stocks..."
		logger.info("Collecting price data for previous day stocks: " + datetime.datetime.today().strftime('%Y-%m-%d'))
		# Send the list to have new price collected
		previous_day_array = collect_fundamental_data(url, previous_day_array, database_array, "aftermath", insert_mode)

		# If no errors returned
		if previous_day_array:
			# Check insert  mode to check if store should be called after array build or items already stored
			if insert_mode == "array":
				# Print message to stdout and log
				print "Sending previous day price data to database for insertion..."
				logger.info("Sending previous day price data to database for insertion: " + datetime.datetime.today().strftime('%Y-%m-%d'))
				# Store new close prices into database()
				store_previous_day_data(database_array, previous_day_array, insert_mode)

# Collect previous day tickers to fill in after SHTF data
def collect_previous_day_tickers(database_array):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	# Create array to store the items from database
	previous_day_data_array = []

	try:
		# Initalize a connection to the database with creds in database_array
		shtf_database_connection = MySQLdb.connect(host=database_array["host"], user=database_array["username"], passwd=database_array["password"], db=database_array['database'])
		shtf_database_connection.autocommit = True
		shtf_connection = shtf_database_connection.cursor()

		# Collect all stocks that have less than 10 days of data entered from database
		query_string = ("SELECT `id`, `ticker`, `metric`, `price_day_2`, `price_day_3`, `price_day_4`, `price_day_5`, `price_day_6`, "
			"`price_day_7`, `price_day_8`, `price_day_9`, `price_day_10` FROM " + database_array['table'] + " WHERE ")
		query_string += "`date` < '" + datetime.datetime.today().strftime('%Y-%m-%d') + "' AND ("
		query_string += "price_day_2 IS NULL "
		query_string += "OR price_day_3 IS NULL "
		query_string += "OR price_day_4 IS NULL "
		query_string += "OR price_day_5 IS NULL "
		query_string += "OR price_day_6 IS NULL "
		query_string += "OR price_day_7 IS NULL "
		query_string += "OR price_day_8 IS NULL "
		query_string += "OR price_day_9 IS NULL "
		query_string += "OR price_day_10 IS NULL "
		query_string += ");"

		# Use the connection to execute the query
		shtf_connection.execute(query_string)
		previous_day_data = shtf_connection.fetchall()
		shtf_database_connection.close()

		# If there are no records that need updating then print message and log
		if len(previous_day_data) == 0:
			# Print message to stdout and log
			print "No previous day data found to require updating: " + datetime.datetime.today().strftime('%Y-%m-%d')
			logger.info("No previous day data found to require updating: " + datetime.datetime.today().strftime('%Y-%m-%d'))
			return False

		for item in previous_day_data:
			previous_day_data_array.append({ "database_id" : str(item[0]), "ticker" : item[1], "metric" : item[2], "price_day_2" : item[3],
			"price_day_3" : item[4], "price_day_4" : item[5], "price_day_5" : item[6], "price_day_6" : item[7], "price_day_7" : item[8],
			"price_day_8" : item[9], "price_day_9" : item[10], "price_day_10" : item[11] })

		# Print message to stdout and log of database entry success
		print "Previous day data collected from database: " + datetime.datetime.today().strftime('%Y-%m-%d')
		logger.info("Previous day data collected from database: " + datetime.datetime.today().strftime('%Y-%m-%d'))

		return previous_day_data_array

	# If collecting from database failed log error and return False
	except Exception as e:
		# Collect the exception information
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# Print the error
		print 'Failed collect data from database : ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
		# Log error with creating filepath
		logger.error('Failed collect data from database: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
		return False

# Used to store the previous day tickers closing  price
def store_previous_day_data(database_array, previous_day_array, insert_mode):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	try:
		# Initalize a connection to the database with creds in database_array
		shtf_database_connection = MySQLdb.connect(host=database_array["host"], user=database_array["username"], passwd=database_array["password"], db=database_array['database'])
		shtf_database_connection.autocommit = True
		shtf_connection = shtf_database_connection.cursor()

		if insert_mode == "array":
			# Look for the next NULL database column to insert values into
			for item in previous_day_array:

				# keep track of next day to enter value into
				next_day = 0

				if item["price_day_2"] == None: next_day = "2"
				elif item["price_day_3"] == None: next_day = "3"
				elif item["price_day_4"] == None: next_day = "4"
				elif item["price_day_5"] == None: next_day = "5"
				elif item["price_day_6"] == None: next_day = "6"
				elif item["price_day_7"] == None: next_day = "7"
				elif item["price_day_8"] == None: next_day = "8"
				elif item["price_day_9"] == None: next_day = "9"
				elif item["price_day_10"] == None: next_day = "10"

				# If the next_day is not 0, then an empty day was found
				if next_day != 0:
					# Build the query string to insert the new price for appropiate day
					query_string = "UPDATE " + database_array['table'] + " "
					query_string += "SET price_day_" + next_day + " = " + item["Price"]
					query_string += " WHERE id=" + item["database_id"] + "; "

					# Use the connection to execute the query
					shtf_connection.execute(query_string)

					# Print message to stdout and log of database entry success
					print "Next day price data entered into database for stock: " + item['ticker']
					logger.info("Next day price data entered into database for stock: " + item['ticker'] + " at " + datetime.datetime.today().strftime('%Y-%m-%d'))

		if insert_mode == "item":

			# Assign the item to a variable to send into database
			item = previous_day_array

			# keep track of next day to enter value into
			next_day = 0

			if item["price_day_2"] == None: next_day = "2"
			elif item["price_day_3"] == None: next_day = "3"
			elif item["price_day_4"] == None: next_day = "4"
			elif item["price_day_5"] == None: next_day = "5"
			elif item["price_day_6"] == None: next_day = "6"
			elif item["price_day_7"] == None: next_day = "7"
			elif item["price_day_8"] == None: next_day = "8"
			elif item["price_day_9"] == None: next_day = "9"
			elif item["price_day_10"] == None: next_day = "10"

			# If the next_day is not 0, then an empty day was found
			if next_day != 0:
				# Build the query string to insert the new price for appropiate day
				query_string = "UPDATE " + database_array['table'] + " "
				query_string += "SET price_day_" + next_day + " = " + item["Price"]
				query_string += " WHERE id=" + item["database_id"] + "; "

				# Use the connection to execute the query
				shtf_connection.execute(query_string)

				# Print message to stdout and log of database entry success
				print "Next day price data entered into database for stock: " + item['ticker']
				logger.info("Next day price data entered into database for stock: " + item['ticker'] + " at " + datetime.datetime.today().strftime('%Y-%m-%d'))


		# Close the database conection
		shtf_database_connection.close()
		# Return success bool
		return True

	# If inserting to database failed log error and return False
	except Exception as e:
		# Collect the exception information
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# Print the error
		print 'Failed insert previous day new price data to database : ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
		# Log error with creating filepath
		logger.error('Failed insert previous day price data to database: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
		return False

# Collect todays list of stocks from web
def collect_today_most_volatile(url):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	# Print intialization message
	print 'Grabbing from: ' + url + '...\n'

	# Begin Scraping from the url provided
	try:
				r = urllib2.urlopen(url)

	# If scraping failed log error and return False
	except urllib2.URLError as e:
		# Collect the exception information
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# Print the error
		print 'Failed to download page from website : ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
		# Log error with creating filepath
		logger.error('Failed to download page from website: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
		return False

	# If the error code from the return is OK
	try:
		if r.code in (200, 401):

			# Log the successful page download
			logger.error('Page download from url successful: ' + url)

			# Create an array to store the volatile stock data
			today_metric_array = []

			# Get the table data from the page
			data = urllib.urlopen(url).read()
			# Send to beautiful soup
			soup = BeautifulSoup(data, "html.parser")
			i=1
			# Find the tables with class t-home-table
			for table in soup("table", { "class" : "t-home-table"}):

				# First and second tables
				if i==1 or i==2:
					for tr in table.findAll('tr')[1:]:
						col = tr.findAll('td')
						# Collect the data from table
						ticker = col[0].get_text().encode('ascii','ignore')
						price = col[1].get_text().encode('ascii','ignore')
						change = col[2].get_text().encode('ascii','ignore')
						volume = col[3].get_text().encode('ascii','ignore')
						metric = col[5].get_text().encode('ascii','ignore')
						record = {"ticker" : ticker, "price" : price, "change" : change, "volume" : volume, "metric" : metric}
						# Output to screen
						#print record
						# Append the array to the list of metric
						today_metric_array.append(record)

				# Third and fourth tables
				if i==3 or i==4:
					for tr in table.findAll('tr')[1:]:
						col = tr.findAll('td')
						ticker1 = col[0].get_text().encode('ascii','ignore')
						ticker2 = col[1].get_text().encode('ascii','ignore')
						ticker3 = col[2].get_text().encode('ascii','ignore')
						ticker4 = col[3].get_text().encode('ascii','ignore')
						metric = col[5].get_text().encode('ascii','ignore')
						record = {"date" : datetime.datetime.today().strftime('%Y-%m-%d'), "ticker1" : ticker1, "ticker2" : ticker2, "ticker3" : ticker3, "ticker4" : ticker4, "metric" : metric}
						# Output to stdout
						#print record
						# Append the array to the list of metric
						today_metric_array.append(record)

				# Increment the table number
				i+=1

		# If the page does not send an acceptable return code
		else:
			# Print to stdout that file returned an error code
			print "The website returned an error code."
			# Log error with return code
			logger.error('The website returned a error code.')
			return False

		# Run array through sanitizer to split up metrics that include more than one ticker
		today_metric_array = sanitize_today_metric_array(today_metric_array)

		# Return the array with all todays metric data
		return today_metric_array

	# If scraping failed log error and return False
	except Exception as e:
			# Collect the exception information
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			# Print the error
			print 'Failed to download page from website : ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
			# Log error with creating filepath
			logger.error('Failed to download page from website: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
			return False

# Sanitize metric array to split up metrics with more than one ticker into separate values
def sanitize_today_metric_array(today_metric_array):

	# Define an array to store checked items
	sanitized_today_metric_array = []
	multiple_ticker_flag = False

	for item in today_metric_array:
		# Check if the key ticker1, ticker2, etc are in the key values
		if "ticker1" in item:
			record_to_append = { "ticker" : item["ticker1"], "metric" : item["metric"]}
			sanitized_today_metric_array.append(record_to_append)
			multiple_ticker_flag = True
		if "ticker2" in item:
			record_to_append = { "ticker" : item["ticker2"], "metric" : item["metric"]}
			sanitized_today_metric_array.append(record_to_append)
			multiple_ticker_flag = True
		if "ticker3" in item:
			record_to_append = { "ticker" : item["ticker3"], "metric" : item["metric"]}
			sanitized_today_metric_array.append(record_to_append)
			multiple_ticker_flag = True
		if "ticker4" in item:
			record_to_append = { "ticker" : item["ticker4"], "metric" : item["metric"] }
			sanitized_today_metric_array.append(record_to_append)
			multiple_ticker_flag = True

		# If no flags for multiple tickers, then just append normally
		if multiple_ticker_flag == False:
			sanitized_today_metric_array.append(item)


	# Finally return the adjusted sanitized metric array
	return sanitized_today_metric_array

# Collect the fundamental data for each stock on the list for today
def collect_fundamental_data(finviz_fundamental_url, today_metric_array, database_array, record_type, insert_mode):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	# Print intialization message
	print 'Starting to collect fundamental data... '

	try:

		# Create an array to store the fundamental data
		fundamentals_array = []

		# For each item in today_metric_array collect fundamental page
		for item in today_metric_array:

			# Define url used in calls to fundamental data page
			url = finviz_fundamental_url + item["ticker"]
			print 'Grabbing fundamental data from: ' + url

			# Download the page with fundamental data
			try:
				r = urllib2.urlopen(url)
			except urllib2.URLError as e:
				r = e

			# Check the return code of the page to check OK
			if r.code in (200, 401):
				# Get the table data from the page
   				data = urllib.urlopen(url).read()
				# Pass to BeautifulSoup html parser
   				soup = BeautifulSoup(data, "html.parser")
				# Set an increment variable for looping through tables
   				i=1
				# Get the correct table into a variable
   				table = soup.find("table", { "class" : "fullview-title"})

				# Loop through the table items
   				for tr in table.findAll('tr')[1:]:
   						if i==1:
   							col = tr.findAll('td')
   							companyname = col[0].get_text().encode('ascii','ignore')
						if i==2:
   							col = tr.findAll('td')
   							industry = col[0].get_text().encode('ascii','ignore')
   						i +=1
	   			companyname = companyname.replace (',','')
	   			industry = industry.replace(',','')
	   			industrylist = industry.split('|')
				industrylist = strip_list(industrylist)
				record = {"ticker": item["ticker"], "date" : datetime.datetime.today().strftime('%Y-%m-%d'), "signal" : item["metric"], 'CompanyName' : companyname, 'Industry' : industrylist[0], 'SubIndustry' : industrylist[1], 'Country' : industrylist[2]}
				# Append the item to array of fundamental data
				item.update(record)
				# Print the updated record to stdout

				# For each row of fundamental data create a dict and update item
				for table in soup("table", { "class" : "snapshot-table2"}):
   					#Large Financial Data Table
   					for tr in table.findAll('tr')[0:]:
						col = tr.findAll('td')
						metric1 = col[0].get_text().encode('ascii','ignore')
						data1 = col[1].get_text().encode('ascii','ignore')
						metric2 = col[2].get_text().encode('ascii','ignore')
						data2 = col[3].get_text().encode('ascii','ignore')
						metric3 = col[4].get_text().encode('ascii','ignore')
						data3 = col[5].get_text().encode('ascii','ignore')
						metric4 = col[6].get_text().encode('ascii','ignore')
						data4 = col[7].get_text().encode('ascii','ignore')
						metric5 = col[8].get_text().encode('ascii','ignore')
						data5 = col[9].get_text().encode('ascii','ignore')
						metric6 = col[10].get_text().encode('ascii','ignore')
						data6 = col[11].get_text().encode('ascii','ignore')
						record = {metric1 : data1, metric2 : data2, metric3 : data3, metric4 : data4, metric5 : data5, metric6 : data6}
						# Append the item to array of fundamental data
						item.update(record)

				# Send the item to be sanitized and some values separated
				item = sanitize_fundamentals_record(item)

				# Finally append the dict item to the fundamental_data_array
				fundamentals_array.append(item)
				print "Fundamental data collection complete for : " + item["CompanyName"]

				# Check here to insert the item to database if flag set to by_item
				if insert_mode == "item":
					if record_type == "shtf":
						store_metrics_data(database_array, item, insert_mode)
					elif record_type == "aftermath":
						store_previous_day_data(database_array, item, insert_mode)


   			#if the page does not return OK code, log error and print to stdout
			else:
				# Print to stdout that file returned an error code
				print "The website returned an error code collecting fundamental data: " + finviz_fundamental_url
				# Log error with return code
				logger.error('The website returned an error code collecting fundamental data: ' + finviz_fundamental_url)
				return False

		# Finally return the fundamentals array
		return fundamentals_array

	# If scraping failed log error and return False
	except Exception as e:
		# Collect the exception information
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# Print the error
		print 'Failed to collect fundamental data from website : ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
		# Log error with creating filepath
		logger.error('Failed to collect fundamental data from website: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
		return False


def sanitize_fundamentals_record(record):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	# Define an array of vales that have descriptive numerical values
	descriptive_numerical_key_array = ["Avg Volume", "Market Cap", "Sales", "Income", "Shs Float", "Shs Outstand"]
	# Define an array of keys to ignore sanitization for (price_day_#)
	ignore_keys_array = ["price_day_2", "price_day_3", "price_day_4", "price_day_5", "price_day_6", "price_day_7", "price_day_8", "price_day_9", "price_day_9", "price_day_10"]

	# Define a dictionary to hold sanitized values
	sanitized_record = {}
	#print record
	# Loop through all values in the record
	for key, value in record.items():
		if value != None and key not in ignore_keys_array:
			# Remove all percent signs
			value = value.replace("%", "")
			# Remove all comma
			value = value.replace(",", "")
			# Remove all whitespace
			value = value.strip()
		# Change all descriptive numerical values to integer numerical values (K,M,B)
		if key in descriptive_numerical_key_array and value.endswith("B"):
			value = value.replace("B", "")
			value = decimal.Decimal(value) * 1000000000
			value = str(value).split(".")[0]
	 	if key in descriptive_numerical_key_array and value.endswith("K"):
			value = value.replace("K", "")
			value = decimal.Decimal(value) * 1000
			value = str(value).split(".")[0]
		if key in descriptive_numerical_key_array and value.endswith("M"):
			value = value.replace("M", "")
			value = decimal.Decimal(value) * 1000000000
			value = str(value).split(".")[0]
		# If value is "-" then make = NULL
		if value == "-": value = None
		#print value
		# Split values that need to be split
		if key == "Volatility":
			volatility_list = record["Volatility"].split()
			#print volatility_list
			# Go through list and remove unwanted characters
			for i,item in enumerate(volatility_list):
				volatility_list[i] = item.strip().replace("%", "")
			sanitized_record.update({ "volatility_low" : volatility_list[0], "volatility_high" : volatility_list[1] })
		elif key == "52W Range":
			_52_W_range_list = record["52W Range"].split("-")
			# Check length of array to look for company without 52 weeks of history
			if len(_52_W_range_list) > 2:
				# Drop the first item in list because the company is new company and does not have 52 weeks of history
				_52_W_range_list.pop(0)
				# if other elements in list have no values then strip them
				for i,item in enumerate(_52_W_range_list):
					_52_W_range_list[i] = item.strip()
					if item.strip() == "":
						_52_W_range_list[i] = None

			#print _52_W_range_list
			sanitized_record.update({ "52_W_range_low" : _52_W_range_list[0], "52_W_range_high" : _52_W_range_list[1]})

		else:
			sanitized_record.update({key : value})
	# Change all thousands, millions, and billions into integer values
	#print sanitized_record
	return sanitized_record

def store_metrics_data(database_array, fundamentals_array, insert_mode):

	# Import logging function
	logger = logging.getLogger("SHTF_stock_screener")

	try:
		# Initalize a connection to the database with creds in database_array
		shtf_database_connection = MySQLdb.connect(host=database_array["host"], user=database_array["username"], passwd=database_array["password"], db=database_array['database'])
		shtf_database_connection.autocommit = True
		shtf_connection = shtf_database_connection.cursor()

		if insert_mode == "array":
			# For each item in the fundamentals_array
			for item in fundamentals_array:
				# Create a query string that will place each item into database
				query_string = "INSERT INTO " + database_array['table'] + " "
				query_string += ("(`metric`,`ticker`,`company_name`,`country`,`industry`,`sub_industry`,`price`,`change_%%`,"
							"`forward_PE`,`index`,`current_ratio`,`inst_trans_%%`,`perf_quarter_%%`,`EPS_next_5_Y_%%`,`shs_float`,`book_sh`,"
							"`P/S`,`quick_ratio`,`salesQ/Q_%%`,`ATR`,`earnings_date`,`inst_own_%%`,`52_W_low_%%`,"
							"`SMA20_%%`,`P/E`,`P/B`,`P/C`,`perf_YTD_%%`,`oper_margin_%%`,`shs_outstand`,`EPS_Q/Q_%%`,`PEG`,`insider_trans_%%`,"
							"`ROA`,`market_cap`,`SMA200_%%`,`ROE`,`52_W_range_high`,`52_W_range_low`,`employees`,`target_price`,`EPS_this_Y_%%`,"
							"`beta`,`short_ratio`,`P/FCF`,`dividend_%%`,`rel_volume`,`perf_year_%%`,`dividend`,`volatility_high_%%`,`volatility_low_%%`,"
							"`payout`,`insider_own_%%`,`prev_close`,`ROI`,`perf_week_%%`,`recom`,`52_W_high_%%`,`EPS_ttm`,`SMA50_%%`,`volume`,"
							"`date`,`short_float_%%`,`perf_month_%%`,`cash/sh`,`shortable`,`LT_debt/eq`,`gross_margin_%%`,`perf_half_Y_%%`,"
							"`EPS_past_5_Y_%%`,`sales`,`EPS_next_Q_%%`,`profit_margin_%%`,`optionable`,`debt/eq`,`EPS_next_Y_%%`,`avg_volume`,"
							"`RSI_14`,`sales_past_5_Y_%%`,`income`)")

				query_string += (" VALUES (%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s,%s,%s,%s,%s,"
				              "%s,%s,%s,%s);")

				# Create an array of values to put into the database
				values_array = []
				values_array.extend([item["metric"], item["ticker"], item["CompanyName"], item['Country'], item['Industry'], item['SubIndustry'], item['Price'], item['Change']])
				values_array.extend([item['Forward P/E'], item['Index'], item["Current Ratio"], item['Inst Trans'], item['Perf Quarter'], item['EPS next 5Y'], item['Shs Float'], item['Book/sh']])
				values_array.extend([item['P/S'], item['Quick Ratio'], item['Sales Q/Q'], item['ATR'], item['Earnings'], item['Inst Own'], item['52W Low']])
				values_array.extend([item['SMA20'], item['P/E'], item['P/B'], item['P/C'], item['Perf YTD'], item['Oper. Margin'], item['Shs Outstand'], item['EPS Q/Q'], item['PEG'], item['Insider Trans']])
				values_array.extend([item['ROA'], item['Market Cap'], item['SMA200'], item['ROE'], item['52_W_range_high'], item['52_W_range_low'], item['Employees'], item['Target Price'], item['EPS this Y']])
				values_array.extend([item['Beta'], item['Short Ratio'], item['P/FCF'], item['Dividend %'], item['Rel Volume'], item['Perf Year'], item['Dividend'], item['volatility_high'], item['volatility_low']])
				values_array.extend([item['Payout'], item['Insider Own'], item['Prev Close'], item['ROI'], item['Perf Week'], item['Recom'], item['52W High'], item['EPS (ttm)'], item['SMA50'], item['Volume']])
				values_array.extend([item['date'], item['Short Float'], item['Perf Month'], item['Cash/sh'], item['Shortable'], item['LT Debt/Eq'], item['Gross Margin'], item['Perf Half Y']])
				values_array.extend([item['EPS past 5Y'], item['Sales'], item['EPS next Q'], item['Profit Margin'], item['Optionable'], item['Debt/Eq'], item['EPS next Y'], item['Avg Volume']])
				values_array.extend([item['RSI (14)'], item['Sales past 5Y'], item['Income']])

				# Use the connection to execute the query
				shtf_connection.execute(query_string, values_array)

				# Print message to stdout and log of database entry success
				print "Fundamentals entered into database for stock: " + item['ticker']
				logger.info("Fundamentals entered into database for stock: " + item['ticker'] + " at " + datetime.datetime.today().strftime('%Y-%m-%d'))


		elif insert_mode == "item":

			# point to variable called item
			item = fundamentals_array

			# Create a query string that will place each item into database
			query_string = "INSERT INTO " + database_array['table'] + " "
			query_string += ("(`metric`,`ticker`,`company_name`,`country`,`industry`,`sub_industry`,`price`,`change_%%`,"
						"`forward_PE`,`index`,`current_ratio`,`inst_trans_%%`,`perf_quarter_%%`,`EPS_next_5_Y_%%`,`shs_float`,`book_sh`,"
						"`P/S`,`quick_ratio`,`salesQ/Q_%%`,`ATR`,`earnings_date`,`inst_own_%%`,`52_W_low_%%`,"
						"`SMA20_%%`,`P/E`,`P/B`,`P/C`,`perf_YTD_%%`,`oper_margin_%%`,`shs_outstand`,`EPS_Q/Q_%%`,`PEG`,`insider_trans_%%`,"
						"`ROA`,`market_cap`,`SMA200_%%`,`ROE`,`52_W_range_high`,`52_W_range_low`,`employees`,`target_price`,`EPS_this_Y_%%`,"
						"`beta`,`short_ratio`,`P/FCF`,`dividend_%%`,`rel_volume`,`perf_year_%%`,`dividend`,`volatility_high_%%`,`volatility_low_%%`,"
						"`payout`,`insider_own_%%`,`prev_close`,`ROI`,`perf_week_%%`,`recom`,`52_W_high_%%`,`EPS_ttm`,`SMA50_%%`,`volume`,"
						"`date`,`short_float_%%`,`perf_month_%%`,`cash/sh`,`shortable`,`LT_debt/eq`,`gross_margin_%%`,`perf_half_Y_%%`,"
						"`EPS_past_5_Y_%%`,`sales`,`EPS_next_Q_%%`,`profit_margin_%%`,`optionable`,`debt/eq`,`EPS_next_Y_%%`,`avg_volume`,"
						"`RSI_14`,`sales_past_5_Y_%%`,`income`)")

			query_string += (" VALUES (%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s,%s,%s,%s,%s,"
			              "%s,%s,%s,%s);")

			# Create an array of values to put into the database
			values_array = []
			values_array.extend([item["metric"], item["ticker"], item["CompanyName"], item['Country'], item['Industry'], item['SubIndustry'], item['Price'], item['Change']])
			values_array.extend([item['Forward P/E'], item['Index'], item["Current Ratio"], item['Inst Trans'], item['Perf Quarter'], item['EPS next 5Y'], item['Shs Float'], item['Book/sh']])
			values_array.extend([item['P/S'], item['Quick Ratio'], item['Sales Q/Q'], item['ATR'], item['Earnings'], item['Inst Own'], item['52W Low']])
			values_array.extend([item['SMA20'], item['P/E'], item['P/B'], item['P/C'], item['Perf YTD'], item['Oper. Margin'], item['Shs Outstand'], item['EPS Q/Q'], item['PEG'], item['Insider Trans']])
			values_array.extend([item['ROA'], item['Market Cap'], item['SMA200'], item['ROE'], item['52_W_range_high'], item['52_W_range_low'], item['Employees'], item['Target Price'], item['EPS this Y']])
			values_array.extend([item['Beta'], item['Short Ratio'], item['P/FCF'], item['Dividend %'], item['Rel Volume'], item['Perf Year'], item['Dividend'], item['volatility_high'], item['volatility_low']])
			values_array.extend([item['Payout'], item['Insider Own'], item['Prev Close'], item['ROI'], item['Perf Week'], item['Recom'], item['52W High'], item['EPS (ttm)'], item['SMA50'], item['Volume']])
			values_array.extend([item['date'], item['Short Float'], item['Perf Month'], item['Cash/sh'], item['Shortable'], item['LT Debt/Eq'], item['Gross Margin'], item['Perf Half Y']])
			values_array.extend([item['EPS past 5Y'], item['Sales'], item['EPS next Q'], item['Profit Margin'], item['Optionable'], item['Debt/Eq'], item['EPS next Y'], item['Avg Volume']])
			values_array.extend([item['RSI (14)'], item['Sales past 5Y'], item['Income']])

			# Use the connection to execute the query
			shtf_connection.execute(query_string, values_array)

			# Print message to stdout and log of database entry success
			print "Fundamentals entered into database for stock: " + item['ticker']
			logger.info("Fundamentals entered into database for stock: " + item['ticker'] + " at " + datetime.datetime.today().strftime('%Y-%m-%d'))

		# Close the database conection
		shtf_database_connection.close()
		# Return success bool
		return True

	# If scraping failed log error and return False
	except Exception as e:
		# Collect the exception information
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# Print the error
		print 'Failed to enter fundamental data to database : ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
		# Log error with creating filepath
		logger.error('Failed to enter fundamental data to database: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
		return False

# Builds arguments output for stdout
def build_argument_output():
	argument_output = "Usage : shtf.py -<mode>\n"
	argument_output += "-h, -help : print help menu\n"
	argument_output += "-daily : set mode to collect new stocks that are posted daily with a metric and collect next day data\n"
	argument_output += "-intra : collects intra daily prices for a selected group of stocks\n"
	argument_output += "-report : build saves and sends a report based on set criteria\n"
	return argument_output

## Parses the command argument sys.arg into command set
def build_command_arguments(argument_array, allowed_args_array):

	## Include logger in the main function
	logger = logging.getLogger("SHTF_stock_screener")

	try:
		# Create an array to store modified command line arguemnts
		command_arg = []

		# Pop off the first element of array because it's the application filename
		argument_array.pop(0)

		# For loop to modify elements and strip "-"
		for item in argument_array:
			if item in allowed_args_array:
				command_arg.append(item.replace('-', ''))

		# The final array should always be list of length 1
		if len(command_arg) != 1:
			print "Only one command line argument is allowed."
			return False
		# Return the modified array of length is proper
		else:
			return command_arg

	except Exception as e:
		# Collect the exception information
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# Print the error
		print 'Failed to build command arguments: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno)
		# Log error with creating filepath
		logger.error('Failed to build command arguments: ' + str(e) + str(exc_type) + str(fname) + str(exc_tb.tb_lineno))
		return False

## MAIN DAILY STOCK SCREENER
##
# This section of the app collects Finviz.com stocks for metrics on the frontpage
# The app scrapes the frontpage and records all the metric name, stock and price data
#
## Main Function Starts Here ##
if __name__ == '__main__':

	# Declare file IO paths and urls
	#
	app_base_filepath = os.getcwd()
	file_name = app_base_filepath + "/data/day1.txt"
	CompanyOutput = app_base_filepath + "/data/FinvizCompanyData.txt"
	AlertOutput = app_base_filepath + "/data/DailyAlerts.txt"
	day2Output = app_base_filepath + "/data/day2.txt"
	data_file = app_base_filepath + "/data"
	log_file = app_base_filepath + "/shtf.log"
	finviz_url = "http://www.finviz.com"
	finviz_fundamental_url = "http://finviz.com/quote.ashx?t="
	previous_days_url = 'http://finviz.com/quote.ashx?t='
	database_array = {"type" : "mysql", "host" : "localhost", "username" : "shtf", "password" : "6Z8zDa^AB6EBJNZ#Vt^&", "port" : "3306", "database" : "shtf", "table" : "shtf_data"}
	# Insert mode is used to set if data is entered into database as each item is parsed, or after the final array is built.
	insert_mode = "item" # values are "item" or "array"
	email_report_to_address = "administrator@company.com"
	email_report = True
	report_to_file = True
	email_server_array = ["smtp.zoho.com", "587", "username", "password", "no-reply@company.com"]
	allowed_args_array = ["-daily", "-daily-close", "-daily-open", "-report", "-intra", "-h", "-help"]

	## Run function to setup logger
	setup_logger(log_file)
	## Include logger in the main function
	logger = logging.getLogger("SHTF_stock_screener")

	## Perform analysis of command line args into another array
	command_arg = build_command_arguments(sys.argv, allowed_args_array)

	## Check return from command line arg bulder and if no command line args
	## print error message and menu
	if command_arg == False or command_arg[0] == "h" or command_arg[0] == "help":
		print "command argument error...."
		## Print out full argument help menu
		print build_argument_output()

	#print command_arg
	# If the argument is "daily" then do activities for daily stock collection
	if command_arg[0] == "daily":
		# Print initialization message to stdout and log
		print 'SHTF Daily Stock Screener Starting... \nScrapign data for ' + datetime.datetime.today().strftime('%Y-%m-%d')
		logger.info('SHTF Daily Stock Screener Started.' + datetime.datetime.today().strftime('%Y-%m-%d'))

		# Collect SHTF data for today
		# Collect today's most volatile stocks from Finviz.com
		today_metric_array = collect_today_most_volatile(finviz_url)

		# If collect today most volatile successful
		if today_metric_array:
			# Print stdout success messgage
			print 'SHTF Stock Screener has collected metrics array for today : ' + datetime.datetime.today().strftime('%Y-%m-%d')
			logger.info('SHTF Stock Screener has collected metrics array for today : ' + datetime.datetime.today().strftime('%Y-%m-%d'))
			print 'SHTF Stock Screener starting to collect fundamental data...'
			# Collect fundamental data for today's most volatile
			fundamentals_array = collect_fundamental_data(finviz_fundamental_url, today_metric_array, database_array, "shtf", insert_mode)

			if fundamentals_array:
				if insert_mode == "array":
					# Print stdout success messgage
					print 'SHTF Stock Screener has collected fundamental data for all companies : ' + datetime.datetime.today().strftime('%Y-%m-%d')
					logger.info('SHTF Stock Screener has collected fundamental data for all companies : ' + datetime.datetime.today().strftime('%Y-%m-%d'))
					print 'SHTF Stock Screener starting to enter data into databas...'
					# Store the fundamental data for todays metrics in database
					store_metrics_success = store_metrics_data(database_array, fundamentals_array, "array")
					if store_metrics_success:
						# Print stdout success messgage
						print 'SHTF Stock Screener has entered all fundamental data for all companies into database : ' + datetime.datetime.today().strftime('%Y-%m-%d')
						logger.info('SHTF Stock Screener has entered all fundamental data for all companies into database : ' + datetime.datetime.today().strftime('%Y-%m-%d'))

		# If collect today most volatile failed
		else:
			print 'SHTF Stock Screener failed to grab from website : ' + finviz_url
			logger.error('SHTF Stock Screener failed to grab from website: ' + finviz_url)


		# Collect data for stocks that were previously SHTF
		# Process previous days most volitile stocks list
		previous_day_success = process_previous_days_new_close(previous_days_url, database_array, insert_mode)
		print 'SHTF Stock Screener has collected aftermath data for all stocks : ' + datetime.datetime.today().strftime('%Y-%m-%d')
		logger.info('SHTF Stock Screener has collected aftermath data for all stocks: ' + datetime.datetime.today().strftime('%Y-%m-%d'))





#log the finished message to the console
print "SHTF Stock screener has completed..."
