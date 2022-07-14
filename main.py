import pandas as pd
from pandas.tseries.offsets import BDay
import pandas_market_calendars as mcal
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as datetime
import time
import schedule

#add readme

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

def perMinute(ticker):
    today = datetime.datetime.today().replace(second = 0, microsecond = 0)

    #twoHundredMinutes = datetime.timedelta(minutes=200)
    #todayMinus = today - twoHundredMinutes
    
    #print("Today", today)
    #print("Today minus 200", todayMinus)

    #Open, High, Low, Close, Volume
    tickerHistoryPerMinute =  ticker.history(period = "202m", interval="1m", actions=False)
 
    print("Per minute", tickerHistoryPerMinute)
    #print("First", tickerHistoryPerMinute.Close[0])
    #print("Last", tickerHistoryPerMinute.Close[200])

    tickerHistoryLength = len(tickerHistoryPerMinute)

    openArray = np.zeros(shape=(tickerHistoryLength, 5))

    for x in range(201):
        openArray[x, 0] = tickerHistoryPerMinute.Open[x]
        openArray[x, 1] = tickerHistoryPerMinute.High[x]
        openArray[x, 2] = tickerHistoryPerMinute.Low[x]
        openArray[x, 3] = tickerHistoryPerMinute.Close[x]
        openArray[x, 4] = tickerHistoryPerMinute.Volume[x]

        #if 0 in openArray[x]:
            #openArray[x] = 0
            
    calculatedFastMA = 0
    calculatedMediumMA = 0
    calculatedSlowMA = 0
    
    calculatedFastEA = 0
    fastEAMultiplier = 2/(20+1)
    previousFastEA = 0
    fastEAInitialValue = openArray[180, 3]
    
    calculatedMediumEA = 0
    mediumEAMultiplier = 2/(50+1)
    previousMediumEA = 0
    mediumEAInitialValue = openArray[150, 3]
    
    calculatedSlowEA = 0
    slowEAMultiplier = 2/(200+1)
    previousSlowEA = 0
    slowEAInitialValue = openArray[0, 3]

    #Calculate the EMA and WMA too
    
    #Calculate fast period moving averages
    for fastPeriod in range(20):
        calculatedFastMA += openArray[200-fastPeriod, 3]
        
        if(fastPeriod == 0):
            calculatedFastEA = (openArray[181, 3] * fastEAMultiplier) + (fastEAInitialValue * (1 - fastEAMultiplier))
        else:
            calculatedFastEA = (openArray[181 + fastPeriod, 3] * fastEAMultiplier) + (previousFastEA * (1 - fastEAMultiplier))
              
        previousFastEA = calculatedFastEA
        
    calculatedFastMA = calculatedFastMA / 20
            
    #Calculate medium period moving averages
    for mediumPeriod in range(50):
        calculatedMediumMA += openArray[200-mediumPeriod, 3]
        
        if(mediumPeriod == 0):
            calculatedMediumEA = (openArray[151, 3] * mediumEAMultiplier) + (mediumEAInitialValue * (1 - mediumEAMultiplier))
        else:
            calculatedMediumEA = (openArray[151 + mediumPeriod, 3] * mediumEAMultiplier) + (previousMediumEA * (1 - mediumEAMultiplier))
              
        previousMediumEA = calculatedMediumEA
        
    calculatedMediumMA = calculatedMediumMA / 50
         
    #Calculate slow period moving averages   
    for slowPeriod in range(200):
        calculatedSlowMA += openArray[200-slowPeriod, 3]
           
        if(slowPeriod == 0):
            calculatedSlowEA = (openArray[1, 3] * slowEAMultiplier) + (slowEAInitialValue * (1 - slowEAMultiplier))
        else:
            calculatedSlowEA = (openArray[1 + slowPeriod, 3] * slowEAMultiplier) + (previousSlowEA * (1 - slowEAMultiplier))
              
        previousSlowEA = calculatedSlowEA
        
    calculatedSlowMA = calculatedSlowMA / 200

    print("Fast Moving Average", calculatedFastMA)
    print("Medium Moving Average", calculatedMediumMA)
    print("Slow Moving Average", calculatedSlowMA)
    
    print("Fast Exponential Moving Average", calculatedFastEA)
    print("Medium Exponential Moving Average", calculatedMediumEA)
    print("Slow Exponential Moving Average", calculatedSlowEA)
    
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

    RSILoopStart = (today - BDay(15))
    RSILoopEnd = (today - BDay(1))

    #twelvePeriodEMA = 0
    #twentySixPeriodEMA  = 0

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
    #[(Previous avg. gain)*13)+ current gain)]/14 should be used for a more exponential calculation

    tickerHistoryLastFourteenDays = ticker.history(start = RSILoopStart, end = RSILoopEnd, interval="1d", actions=False)
    
    #print(tickerHistoryLastFourteenDays)

    totalGain = 0
    totalLoss = 0
    for z in range(0, 14):
        priceDifference = tickerHistoryLastFourteenDays.Close[z+1] - tickerHistoryLastFourteenDays.Close[z]
        
        if(priceDifference > 0):
            totalGain += priceDifference
            
        if(priceDifference < 0):
            totalLoss += priceDifference
    
    averageGain = totalGain / 14
    averageLoss = (totalLoss / 14) * -1
            
    relativeStrength = averageGain / averageLoss

    #Need to calculate smoothed RSI
    relativeStrengthIndex = 100 - (100 / (1 + relativeStrength))

    #Implement MACD
    print("Relative Strength Index", relativeStrengthIndex)

#--------------------------------------------------------------------------------------------------------------------

def main():
    #need to add scheduling so perDay is called each day
    #only called on valid trading days (use pandas_market_calendars)
    
    stock = "AMD" 
    ticker = yf.Ticker(stock)
    perMinute(ticker)
    perDay(ticker)

#--------------------------------------------------------------------------------------------------------------------

#def populateDatabase(stock):
    #check if database for ticker exists
        #if not, create and populate with historical data from 2000?

    #check if database is up to date
        #if not populate with missing values

#--------------------------------------------------------------------------------------------------------------------

main()