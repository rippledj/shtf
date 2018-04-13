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
import datetime
import csv
import urllib
from bs4 import BeautifulSoup
import urllib2
import MySQLdb
import time

# Function
#
#
def strip_list(the_list):
	return [line.strip() for line in the_list]

#Add sleep between each full page stock download... 20 seconds?
time.sleep(0)

## PREVIOUS 10 DAY STOCK SCREENER
##
# This section of the apps downloads closing prices for stocks
# that made the finviz homepage for various metrics in the past 10 days
#

# variables used in setting paths for file IO
#
path = "/Users/ripple/Dropbox/Python/shtf/data/"
baseurl = 'http://www.nasdaq.com/symbol/'
urltail = '/real-time#.UXA2Iytlei0'
#Read the file and send to MySQL
db=MySQLdb.Connection(host = "127.0.0.1",
                        port = 3306,
                        user = "shtf",
                        passwd = "",
                        db = "shtf")
db.autocommit(True)
db = db.cursor()

# move through files that are listed Day10.txt backwards to Day1.txt
for x in range (10,1,-1):
	stockcsv = csv.reader(open(path + 'day' + str(x) + '.txt','r'))
	num = x+1
	if x < 10:
		moveto = open(path + 'day' + str(x+1) + '.txt','w')
	for row in stockcsv:
		print 'Getting current data for ' + row[0] + ' ' + row[1] + ' ' + row[2] + ' ...'
		stock = row[0]
		date = row[1]
		signal = row[2]
		#go to google or yahoo and get todays price
		url = baseurl + row[0] + urltail
		print "Grabbing " + url
		data = urllib.urlopen(url).read()
		#send to beautiful soup
		soup = BeautifulSoup(data)
		price = soup.find("div", { "class" : "qwidget-dollar" })
		try:
					price = price.get_text().encode('utf-8','ignore').replace('$','')
					price = float(str(price))
		except:
					price = 0.00
		price = "%0.2f" % (price)
		price = str(price)
		add_d2data = ("UPDATE Finviz.VOLATILE SET VOLATILE.D" + str(x) + 'Price = %s WHERE stock = %s AND fdate = %s AND Metric = %s ')
		data_d2data = (price, stock, date, signal)
		db.execute (add_d2data, data_d2data)
		print "Today's price: " + price + ' has been updated in Finviz.VOLATILE.D' + str(x) + 'Price'
		#write the new price to the MySQL database Finviz, Volatile table
		if x < 10:
			#openthisfile = file_name + 'day' + str(num)
			#moveto = open(openthisfile, 'w')
			print "Moving " + row[0] + ' ' + row[1] + ' ' + row[2] + ' ...'
			try:
						moveto.write(row[0] + ',' + row[1] + ',' + row[2] + '\n')
			except:
						pass
	print 'Day ' + str(x) + ' is finished'
	try:
				moveto.close()
	except:
				pass
