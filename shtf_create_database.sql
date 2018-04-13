--
-- Create and Use the SHTF Database
--

DROP DATABASE IF EXISTS `shtf`;
CREATE DATABASE `shtf` CHARACTER SET UTF8mb4 COLLATE UTF8mb4_unicode_ci;
USE `shtf`;

--
-- Create SHTF database
--

DROP TABLE IF EXISTS `shtf_data`;

CREATE TABLE `shtf_data` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`metric` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The metric the company fell under during volatility',
`ticker` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The company ticker on stock market',
`company_name` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The registered name of the company',
`country` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Registered country of the company',
`industry` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'industry of the companies products or services',
`sub_industry` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'subindustry of the companies products or sevices',
`price` decimal(12,2) DEFAULT NULL COMMENT 'price at close of stock on shtf day',
`change_%` decimal(12,2) DEFAULT NULL COMMENT 'percent change in stock price at closing on SHTF day',
`forward_PE` decimal(12,2) DEFAULT NULL COMMENT 'current stock''s price over its "predicted" earnings per share.',
`index` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The stock ticker index',
`current_ratio` decimal(12,2) DEFAULT NULL COMMENT 'mainly used to give an idea of a company''s ability to pay back its liabilities (debt and accounts payable) with its assets (cash, marketable securities, inventory, accounts receivable). As such, current ratio can be used to make a rough estimate of a company''s financial health.',
`inst_trans_%` decimal(12,2) DEFAULT NULL COMMENT 'The amount of a company''s available stock owned by mutual or pension funds, insurance companies, investment firms, private foundations, endowments or other large entities that manage funds on the behalf of others.',
`perf_quarter_%` decimal(12,2) DEFAULT NULL COMMENT 'The quarterly earnings report is a quarterly filing made by public companies to report their performance. Earnings reports include items such as net income, earnings per share, earnings from continuing operations and net sales.',
`EPS_next_5_Y_%` decimal(12,2) DEFAULT NULL COMMENT 'To calculate the EPS of a company, the balance sheet and income statement should be used to find the total number of shares outstanding, dividends on preferred stock (if any), and the net income or profit value.',
`shs_float` bigint(50) DEFAULT NULL COMMENT 'Floating stock is calculated by subtracting closely-held shares and restricted stock from a firm''s total outstanding shares. Closely-held shares are those owned by insiders, major shareholders and employees, while restricted stock refers to insider shares that cannot be traded because of a temporary restriction.',
`book_sh` decimal(12,2) DEFAULT NULL COMMENT 'Book value of an asset is the value at which the asset is carried on a balance sheet and calculated by taking the cost of an asset minus the accumulated depreciation. Book value is also the net asset value of a company, calculated as total assets minus intangible assets (patents, goodwill) and liabilities.',
`P/S` decimal(12,2) DEFAULT NULL COMMENT 'It can be calculated either by dividing the company''s market capitalization by its total sales over a 12-month period, or on a per-share basis by dividing the stock price by sales per share for a 12-month period. ',
`quick_ratio` decimal(12,2) DEFAULT NULL COMMENT 'The quick ratio is a measure of how well a company can meet its short-term financial liabilities. Also known as the acid-test ratio, it can be calculated as follows: (Cash + Marketable Securities + Accounts Receivable) / Current Liabilities.',
`salesQ/Q_%` decimal(12,2) DEFAULT NULL COMMENT 'An increase of a company''s sales when compared to a previous quarter''s revenue performance. AKA Quarterly revenue growth.',
`ATR` decimal(12,2) DEFAULT NULL COMMENT 'The average true range (ATR) is a measure of volatility. The true range indicator is the greatest of the following: current high less the current low, the absolute value of the current high less the previous close and the absolute value of the current low less the previous close. The average true range is a moving average, generally 14 days, of the true ranges. ',
`earnings_date` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Earnings announcement is an official public statement of a company''s profitability for a specific time period, typically a quarter or a year. An earnings announcement is typically made on a specific date during earnings season and is preceded by earnings estimates issued by equity analysts.',
`inst_own_%` decimal(12,2) DEFAULT NULL COMMENT 'Institutional ownership refers to the ownership stake in a company that is held by large financial organizations, pension funds or endowments. Institutions generally purchase large blocks of a company''s outstanding shares and can exert considerable influence upon its management.',
`52_W_low_%` decimal(12,2) DEFAULT NULL COMMENT 'A 52-week high/low is the highest and lowest price that a stock has traded at during the previous year. Many traders and investors view the 52-week high or low as an important factor in determining a stock''s current value and predicting future price movement.',
`SMA20_%` decimal(12,2) DEFAULT NULL COMMENT 'A simple moving average (SMA) is an arithmetic moving average calculated by adding the closing price of the security for a number of time periods and then dividing this total by the number of time periods. As shown in the chart above, many traders watch for short-term averages to cross above longer-term averages',
`P/E` decimal(12,2) DEFAULT NULL COMMENT 'The Price-to-Earnings Ratio or P/E ratio is a ratio for valuing a company that measures its current share price relative to its per-share earnings.',
`P/B` decimal(12,2) DEFAULT NULL COMMENT 'The price-to-book ratio (P/B Ratio) is a ratio used to compare a stock''s market value to its book value. It is calculated by dividing the current closing price of the stock by the latest quarter''s book value per share.',
`P/C` decimal(12,2) DEFAULT NULL COMMENT 'The put-call ratio is a popular tool specifically designed to help individual investors gauge the overall sentiment (mood) of the market. The ratio is calculated by dividing the number of traded put options by the number of traded call options.',
`perf_YTD_%` decimal(12,2) DEFAULT NULL COMMENT 'Year to date (YTD) refers to the period beginning the first day of the current calendar year or fiscal year up to the current date.',
`oper_margin_%` decimal(12,2) DEFAULT NULL COMMENT 'Operating margin is a margin ratio used to measure a company''s pricing strategy and operating efficiency. Operating margin is a measurement of what proportion of a company''s revenue is left over after paying for variable costs of production such as wages, raw materials, etc.',
`shs_outstand` bigint(50) DEFAULT NULL COMMENT 'Outstanding shares refer to a company''s stock currently held by all its shareholders, including share blocks held by institutional investors and restricted shares owned by the company''s officers and insiders. Outstanding shares are shown on a company''s balance sheet under the heading “Capital Stock.”',
`EPS_Q/Q_%` decimal(12,2) DEFAULT NULL COMMENT 'To calculate the EPS of a company, the balance sheet and income statement should be used to find the total number of shares outstanding, dividends on preferred stock (if any), and the net income or profit value.',
`PEG` decimal(12,2) DEFAULT NULL COMMENT 'Price/Earnings to Growth (PEG) is a stock''s price to earnings ratio divided by the growth rate of its earnings for a specified time period.',
`insider_trans_%` decimal(12,2) DEFAULT NULL COMMENT '''Insider Buying'' The purchase of shares of stock in a corporation by someone who is employed by the company.',
`ROA` decimal(12,2) DEFAULT NULL COMMENT 'ROA = Net Income / Total Assets',
`market_cap` bigint(50) DEFAULT NULL COMMENT 'Market capitalization refers to the total dollar market value of a company''s outstanding shares.',
`SMA200_%` decimal(12,2) DEFAULT NULL COMMENT 'A simple moving average (SMA) is an arithmetic moving average calculated by adding the closing price of the security for a number of time periods and then dividing this total by the number of time periods. As shown in the chart above, many traders watch for short-term averages to cross above longer-term averages',
`ROE` decimal(12,2) DEFAULT NULL COMMENT 'Investors use Return on Equity (ROE) calculations to determine how much profit a company generates relative to its total amount of shareholder equity.',
`52_W_range_low` decimal(12,2) DEFAULT NULL COMMENT 'A 52-week high/low is the highest and lowest price that a stock has traded at during the previous year. Many traders and investors view the 52-week high or low as an important factor in determining a stock''s current value and predicting future price movement.',
`52_W_range_high` decimal(12,2) DEFAULT NULL COMMENT 'A 52-week high/low is the highest and lowest price that a stock has traded at during the previous year. Many traders and investors view the 52-week high or low as an important factor in determining a stock''s current value and predicting future price movement.',
`employees` bigint(50) DEFAULT NULL COMMENT 'Total number of employees of a company',
`target_price` decimal(12,2) DEFAULT NULL COMMENT 'A price target is the projected price level of a financial security stated by an investment analyst or advisor. It represents a security''s price that, if achieved, results in a trader recognizing the best possible outcome for his investment.',
`EPS_this_Y_%` decimal(12,2) DEFAULT NULL COMMENT 'Basic EPS is calculated as follows: Basic EPS = (net income – preferred dividends) / weighted average number of common shares outstanding.',
`beta` decimal(12,2) DEFAULT NULL COMMENT 'Beta is a measure of the volatility, or systematic risk, of a security or a portfolio in comparison to the market as a whole. Beta is used in the capital asset pricing model (CAPM), a model that calculates the expected return of an asset based on its beta and expected market returns.',
`short_ratio` decimal(12,2) DEFAULT NULL COMMENT 'The short interest ratio is a sentiment indicator that is derived by dividing the short interest by the average daily volume for a stock. Also known as the days to cover ratio, it is used by both fundamental and technical traders to identify the prevailing sentiment the market has for a specific stock.',
`P/FCF` decimal(12,2) DEFAULT NULL COMMENT 'A valuation metric that compares a company''s market price to its level of annual free cash flow. This is similar to the valuation measure of price-to-cash flow but uses the stricter measure of free cash flow, which reduces operating cash flow by capital expenditures.',
`dividend_%` decimal(12,2) DEFAULT NULL COMMENT 'The dividend yield or dividend-price ratio of a share is the dividend per share, divided by the price per share. It is also a company''s total annual dividend payments divided by its market capitalization, assuming the number of shares is constant. It is often expressed as a percentage.',
`rel_volume` decimal(12,2) DEFAULT NULL COMMENT 'Relative Volume. This compares current volume to normal volume for the same time of day, and it''s displayed as a ratio. So for example, a stock trading 5 1/2 times its normal volume would have a Relative Volume display of 5.5',
`perf_year_%` decimal(12,2) DEFAULT NULL COMMENT 'Performance 1 Year = Last 252 trading days',
`dividend` decimal(12,2) DEFAULT NULL COMMENT 'The dividend yield equals the annual dividend per share divided by the stock’s price. This measurement tells what percentage return a company pays out to shareholders in the form of dividends. Investors who require a minimum stream of cash flow from their investment portfolio can secure this cash flow by investing in stocks paying relatively high, stable dividend yields.\nThe dividend yield equals the annual dividend per share divided by the stock’s price. \nThe dividend yield equals the annual dividend per share divided by the stock’s price. This measurement tells what percentage return a company pays out to shareholders in the form of dividends. Investors who require a minimum stream of cash flow from their investment portfolio can secure this cash flow by investing in stocks paying relatively high, stable dividend yields.\n',
`volatility_low_%` decimal(12,2) DEFAULT NULL COMMENT 'A technical indicator used to identify price ranges and breakouts. The volatility ratio uses a true price range to determine a stock''s true trading range and is able to identify situations where the price has moved out of this true range.',
`volatility_high_%` decimal(12,2) DEFAULT NULL COMMENT 'A technical indicator used to identify price ranges and breakouts. The volatility ratio uses a true price range to determine a stock''s true trading range and is able to identify situations where the price has moved out of this true range.',
`payout` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'With dividends, payouts are made by corporations to their investors and can be in the form of cash dividends or stock dividends. The payout ratio is the percentage rate of income the company pays out to investors in the form of distributions.',
`insider_own_%` decimal(12,2) DEFAULT NULL COMMENT 'Many value investors look for stocks with a high percent of insider ownership, under the theory that when management are shareholders, they will act in its own self interest, and create shareholder value in the long-term. This aligns the interests of shareholders with management, thus benefiting everyone.',
`prev_close` decimal(12,2) DEFAULT NULL COMMENT 'Previous close can refer to the prior day''s value of a stock, bond, commodity, futures or option contract, market index, or any other security. By comparing a security''s closing price from one day to the next, investors can see how the security''s price has changed over time.',
`ROI` decimal(12,2) DEFAULT NULL COMMENT 'A performance measure used to evaluate the efficiency of an investment or to compare the efficiency of a number of different investments. ROI measures the amount of return on an investment relative to the investment''s cost. To calculate ROI, the benefit (or return) of an investment is divided by the cost of the investment,',
`perf_week_%` decimal(12,2) DEFAULT NULL COMMENT 'Performance 1 Week = Last 5 trading days',
`recom` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'An outlook of a stock-market analyst on a stock.',
`52_W_high_%` decimal(12,2) DEFAULT NULL COMMENT 'High: Maximum of the highs during last n-periods (20-day, 50-day, 52-week) expressed as a percentage of the average stock price over the same period.',
`EPS_ttm` decimal(12,2) DEFAULT NULL COMMENT 'Total Earnings / Total Common Shares Outstanding (trailing twelve months)',
`SMA50_%` decimal(12,2) DEFAULT NULL COMMENT 'A simple moving average (SMA) is an arithmetic moving average calculated by adding the closing price of the security for a number of time periods and then dividing this total by the number of time periods. As shown in the chart above, many traders watch for short-term averages to cross above longer-term averages',
`volume` bigint(50) DEFAULT NULL COMMENT 'Volume is an important indicator in technical analysis as it is used to measure the relative worth of a market move. If the markets make a strong price movement, then the strength of that movement depends on the volume for that period. The higher the volume during the price move, the more significant the move.',
`date` date DEFAULT NULL COMMENT 'Date that the data was scraped on.',
`short_float_%` decimal(12,2) DEFAULT NULL COMMENT 'The number of shares short divided by total amount of shares float, expressed in %.',
`perf_month_%` decimal(12,2) DEFAULT NULL COMMENT 'Performance 1 Month = Last 21 trading days',
`cash/sh` decimal(12,2) DEFAULT NULL COMMENT 'Cash per share is the percentage of a firm''s share price that is immediately accessible for spending on activities such as research and development, mergers and acquisitions, purchasing assets, paying down debt, buying back shares and making dividend payments to shareholders.',
`shortable` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'If short shares are available for the company',
`LT_debt/eq` decimal(12,2) DEFAULT NULL COMMENT 'The ratio is calculated by taking the company''s long-term debt and dividing it by the book value of common equity. The greater a company''s leverage, the higher the ratio. Generally, companies with higher ratios are thought to be more risky.',
`gross_margin_%` decimal(12,2) DEFAULT NULL COMMENT 'A company''s total sales revenue minus its cost of goods sold, divided by the total sales revenue, expressed as a percentage. The gross margin represents the percent of total sales revenue that the company retains after incurring the direct costs associated with producing the goods and services sold by a company. The higher the percentage, the more the company retains on each dollar of sales to service its other costs and obligations.',
`perf_half_Y_%` decimal(12,2) DEFAULT NULL COMMENT 'Performance 1/2 Year = Last 176 trading days',
`EPS_past_5_Y_%` decimal(12,2) DEFAULT NULL COMMENT 'To calculate the EPS of a company, the balance sheet and income statement should be used to find the total number of shares outstanding, dividends on preferred stock (if any), and the net income or profit value.',
`sales` bigint(50) DEFAULT NULL COMMENT 'Sales are the proceeds from the provision of goods or services to customers, but this doesn''t capture all of the sources of income for most firms.',
`EPS_next_Q_%` decimal(12,2) DEFAULT NULL COMMENT 'To calculate the EPS of a company, the balance sheet and income statement should be used to find the total number of shares outstanding, dividends on preferred stock (if any), and the net income or profit value.',
`profit_margin_%` decimal(12,2) DEFAULT NULL COMMENT 'Profit margins are expressed as a percentage and, in effect, measure how much out of every dollar of sales a company actually keeps in earnings. A 20% profit margin, then, means the company has a net income of $0.20 for each dollar of total revenue earned.',
`optionable` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'A stock that has options trading on a market exchange. Not all companies that trade publicly have exchange traded options, this is due to requirements that need to be met, such as minimum share price and minimum outstanding shares.',
`debt/eq` decimal(12,2) DEFAULT NULL COMMENT 'Compares total liabilities to shareholders'' equity.',
`EPS_next_Y_%` decimal(12,2) DEFAULT NULL COMMENT 'To calculate the EPS of a company, the balance sheet and income statement should be used to find the total number of shares outstanding, dividends on preferred stock (if any), and the net income or profit value.',
`avg_volume` bigint(50) DEFAULT NULL COMMENT 'The average number of shares traded in a security per day, during the recent 3-month period.',
`RSI_14` decimal(12,2) DEFAULT NULL COMMENT 'The level of the RSI is a measure of the stock''s recent trading strength. The slope of the RSI is directly proportional to the velocity of a change in the trend. The distance traveled by the RSI is proportional to the magnitude of the move. calculated using an n-period smoothed or modified moving average (SMMA or MMA) which is an exponentially smoothed Moving Average with α = 1/period. Some commercial packages, like AIQ, use a standard exponential moving average (EMA) as the average instead of Wilder''s SMMA.',
`sales_past_5_Y_%` decimal(12,2) DEFAULT NULL COMMENT 'Anual sales increase over past 5 years. ',
`income` bigint(50) DEFAULT NULL COMMENT 'Income is money that an individual or business receives in exchange for providing a good or service or through investing capital.',
`price_day_2` decimal(12,2) DEFAULT NULL,
`price_day_3` decimal(12,2) DEFAULT NULL,
`price_day_4` decimal(12,2) DEFAULT NULL,
`price_day_5` decimal(12,2) DEFAULT NULL,
`price_day_6` decimal(12,2) DEFAULT NULL,
`price_day_7` decimal(12,2) DEFAULT NULL,
`price_day_8` decimal(12,2) DEFAULT NULL,
`price_day_9` decimal(12,2) DEFAULT NULL,
`price_day_10` decimal(12,2) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='shtf data';

CREATE TABLE IF NOT EXISTS `shtf`.`shtf_interval_data`(
`id` int(11) COLLATE utf8_unicode_ci NOT NULL AUTO_INCREMENT,
`date` date COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'date that the intraday data is collected for',
`ticker` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The company ticker on stock market',
`time_interval` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'the interval of time that the stock price has been collected for',
`prices` varchar(5000) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'comma separated list of prices per the time_interval field',
PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='shtf inter-day interval price data';


--
-- Create users and permissions for SHTF database configuration
--

-- First Flush all privileges from mysql
FLUSH PRIVILEGES;

-- Set the password function to use mysql_native_password
SET old_passwords = 0;

-- Create and set password for shtf@localhost
DROP USER IF EXISTS 'shtf'@'localhost';
CREATE USER IF NOT EXISTS 'shtf'@'localhost' IDENTIFIED WITH mysql_native_password BY '6Z8zDa^AB6EBJNZ#Vt^&';

-- Grant privileges to all corresponding databases
GRANT SELECT, INSERT, UPDATE ON `shtf`.* TO 'shtf'@'localhost';
