import pandas as pd
from pandas.tseries.offsets import BDay
import pandas_market_calendars as mcal
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as datetime
import time
import schedule

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

    twoHundredMinutes = datetime.timedelta(minutes=200)
    todayMinus = today - twoHundredMinutes
    
    print("Today", today)
    print("Today minus 200", todayMinus)

    #Open, High, Low, Close, Volume
    tickerHistoryPerMinute =  ticker.history(start = todayMinus, end = today, interval="1m", actions=False)
 
    print(tickerHistoryPerMinute)

    tickerHistoryLength = len(tickerHistoryPerMinute)

    openArray = np.zeros(shape=(tickerHistoryLength, 5))

    calculatedFastMA = 0
    calculatedMediumMA = 0
    calculatedSlowMA = 0

    for x in range(200):
        openArray[x, 0] = tickerHistoryPerMinute.Open[x]
        openArray[x, 1] = tickerHistoryPerMinute.High[x]
        openArray[x, 2] = tickerHistoryPerMinute.Low[x]
        openArray[x, 3] = tickerHistoryPerMinute.Close[x]
        openArray[x, 4] = tickerHistoryPerMinute.Volume[x]

        #if 0 in openArray[x]:
            #openArray[x] = 0

    #Calculate the EMA and WMA too
    for fastPeriod in range(20):
        calculatedFastMA += openArray[199-fastPeriod, 3]
        
    calculatedFastMA = calculatedFastMA / 20
            
    for mediumPeriod in range(50):
        calculatedMediumMA += openArray[199-mediumPeriod, 3]
        
    calculatedMediumMA = calculatedMediumMA / 50
            
    for slowPeriod in range(200):
           calculatedSlowMA += openArray[199-slowPeriod, 3]
        
    calculatedSlowMA = calculatedSlowMA / 200

    print("Fast Moving Average", calculatedFastMA)
    print("Medium Moving Average", calculatedMediumMA)
    print("Slow Moving Average", calculatedSlowMA)
    
#--------------------------------------------------------------------------------------------------------------------

def perDay(ticker):
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
            
    if(startCheck == False):
        RSILoopStart = (RSILoopStart - BDay(1))
        
    if(len(nyseValidDays) <= 14):
        RSILoopStart = (RSILoopStart - BDay(1))

    #print("RSI Loop Start 2", RSILoopStart)
    #print("RSI Loop End 2", RSILoopEnd)

    tickerHistoryLastFourteenDays = ticker.history(start = RSILoopStart, end = RSILoopEnd, interval="1d", actions=False)

    percentGain = 0
    percentLoss = 0
    for z in range(1, 15):
        priceDifference = tickerHistoryLastFourteenDays.Close[z] - tickerHistoryLastFourteenDays.Close[z-1]
        
        if(priceDifference > 0):
            percentGain += (priceDifference / tickerHistoryLastFourteenDays.Close[z-1])*100
            
        if(priceDifference < 0):
            percentLoss += (priceDifference / tickerHistoryLastFourteenDays.Close[z-1])*100

    averagePercentGain = percentGain / 14
    averagePercentLoss = (percentLoss / 14) * -1
            
    relativeStrength = averagePercentGain / averagePercentLoss

    #Need to calculate smoothed RSI
    relativeStrengthIndex = 100 - (100 / (1 + relativeStrength))

    #Implement MACD

    #print("Average Percent Gain", averagePercentGain)
    #print("Average Percent Loss", averagePercentLoss)
    #print("Relative Strength", relativeStrength)
    print("Relative Strength Index", relativeStrengthIndex)

#--------------------------------------------------------------------------------------------------------------------

def main():
    #need to add scheduling so perDay is called each day
    #only called on valid trading days (use pandas_market_calendars)
    
    start = time.time()
    stock = "AMD" 
    ticker = yf.Ticker(stock)
    perMinute(ticker)
    perDay(ticker)
    end = time.time()
    print("Time Taken", end-start)

#--------------------------------------------------------------------------------------------------------------------

main()