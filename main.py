import pandas as pd
from pandas.tseries.offsets import BDay
import pandas_market_calendars as mcal
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as datetime
import time
import schedule
from stock import Stock

#add readme

#--------------------------------------------------------------------------------------------------------------------

# Currently calculates: - per minute; 20 period EA and SMA, 50 period EA and SMA, 200 period EA and SMA
#                       - per day; 14 period RSI, MACD

#--------------------------------------------------------------------------------------------------------------------

# Need to implement a function called every minute to calculate the 200 minute array, the SMA, EMA

# Need to implement a function that will be called once per day to calulate RSI, MACD, Bollinger Bands?

# Implement multi-threading to do both at same time?

# Need to implement function to write values to database

# Need to implement a function that will loop through dates to create the dataset for training

# Need to implement funtion that checks the database on runtime and updates values to current

# Need to implement machine learning algorithm to detect when to buy and sell, using database values

# Need to implement buying and selling actual stocks

#--------------------------------------------------------------------------------------------------------------------

# Function works by checking if a minute has passed
# If minute has passed then run functions to calculated fundamentals
# Append these fundamentals to database
# Run machine learning algorithm on latest row of database
# Buy and sell stock based on algorithm
# Profit :)
    
#--------------------------------------------------------------------------------------------------------------------

def perDay(ticker):
    #check if actual trading day
    
    #stockList = ["AMD", "TSLA", "MSFT", "AMZN"]
    #for stock in stockList:
        #check database
        #ticker = yf.Ticker(stock)
        #calculate per day with ticker
        #perMinute(ticker)
    
    today = datetime.datetime.today().replace(hour = 16, minute = 00, second = 0, microsecond = 0)

    #Currently not used
    RSILoopStart = (today - BDay(116))
    RSILoopEnd = (today - BDay(1))
    
    #print("RSI Start", RSILoopStart)
    #print("RSI End", RSILoopEnd)

    nyse = mcal.get_calendar('NYSE')
    nyseValidDays = nyse.valid_days(start_date=RSILoopStart, end_date=RSILoopEnd)

    endCheck = False
    startCheck = False

    for p in range(len(nyseValidDays)):
        if(RSILoopEnd.strftime("%Y-%m-%d") == nyseValidDays[p].strftime("%Y-%m-%d")):
            endCheck = True

        if(RSILoopStart.strftime("%Y-%m-%d") == nyseValidDays[p].strftime("%Y-%m-%d")):
            startCheck = True
            
    if(endCheck == False):
        RSILoopStart = (RSILoopStart - BDay(1))
        RSILoopEnd = (RSILoopEnd - BDay(1))
       
    #this check will be depreceated as the function will not be called when it's not a trading day     
    if(startCheck == False):
        RSILoopStart = (RSILoopStart - BDay(1))
        
    if(len(nyseValidDays) <= 14):
        RSILoopStart = (RSILoopStart - BDay(1))
        
    #RSI calculation is currently wrong
    #Works for calculating RSI for the first 14 days of a stock, but needs to use a more exponential version after
    #[(Previous avg. gain)*13)+ current gain)]/14 is then used for a 30 day smoothed RSI
    
    perDayLoopStart = (today - BDay(120))
    perDayLoopEnd = (today - BDay(1))
    
    #print("Start", perDayLoopStart)
    #print("End", perDayLoopEnd)
    
    

#--------------------------------------------------------------------------------------------------------------------

def main():
    #need to add scheduling so perDay is called each day
    #only called on valid trading days (use pandas_market_calendars)

    date = datetime.datetime.today().replace(hour = 16, minute = 00, second = 0, microsecond = 0)
    stock = "AMD"

    amd = Stock()
    amd.perDay(date, stock)
    amd.perMinute(date, stock)
    
#--------------------------------------------------------------------------------------------------------------------

#def populateDatabase(stock):
    #check if database for ticker exists
        #if not, create and populate with historical data from 2000?

    #check if database is up to date
        #if not populate with missing values

#--------------------------------------------------------------------------------------------------------------------

main()