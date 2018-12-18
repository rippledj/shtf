#USPTO PATENT DATA PARSER

**Author:** Joseph Lee

**Email:** joseph.lee.esl@gmail.com

Description:
------------
This app scrapes the daily stock data from the front page of finviz.com.
The app needs to be scheduled to run after the stock market closes each day (~9pm EST).
The app then collects the financial data from each stocks homepage at finviz.com.
The app also tracks the stocks for 10 days and records daily price closes.
The data is entered into a MySQL database for later analysis.

To see the command line description: $ python shtf.py -help

**The usage of the script is outlined below:**

Instructions:
-------------
There are only two steps.  They are outlined below.

**(1)** - Run the database creation script in MySql (shtf_create_database.sql).

**(2)** - Cron the script.

00 18 * * 1-5 python /path/to/SHTF/shtf.py -daily
