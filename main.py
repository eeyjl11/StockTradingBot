import pandas as pd
from pandas.tseries.offsets import BDay
import pandas_market_calendars as mcal
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as datetime
import time

#Need to implement a function called every minute to calculate the 200 minute array, the SMA, EMA

#Need to implement a function that will be called once per day to calulate RSI, MACD, Bollinger Bands?

#Need to implement function to write values to .csv

#Need to implement a function that will loop through dates to create the dataset for training

#--------------------------------------------------------------------------------------------------------------------

def perMinuteFundamentals(stock):
    amd = yf.Ticker(stock)
    
    today = datetime.datetime.today()
    twoHundredMinutes = datetime.timedelta(minutes=199)
    todayMinus = today - twoHundredMinutes
    
    print("Today", today)
    print("Today minus 200", todayMinus)

    #Open, High, Low, Close, Volume
    amdHistoryPerMinute = amd.history(period="199m", interval="1m", actions=False)

    print(amdHistoryPerMinute)

    amdHistoryLength = len(amdHistoryPerMinute)

    openArray = np.zeros(shape=(amdHistoryLength, 5))

    calculatedFastMA = 0
    calculatedMediumMA = 0
    calculatedSlowMA = 0

    for x in range(200):
        openArray[x, 0] = amdHistoryPerMinute.Open[x]
        openArray[x, 1] = amdHistoryPerMinute.High[x]
        openArray[x, 2] = amdHistoryPerMinute.Low[x]
        openArray[x, 3] = amdHistoryPerMinute.Close[x]
        openArray[x, 4] = amdHistoryPerMinute.Volume[x]

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

def perDayFundamentals(stock):
    amd = yf.Ticker(stock)

    today = datetime.datetime.today().replace(hour = 16, minute = 00, second = 0, microsecond = 0)

    RSILoopStart = (today - BDay(15))
    RSILoopEnd = (today - BDay(1))

    #twelvePeriodEMA = 0
    #twentySixPeriodEMA  = 0

    #print("RSI Loop Start 1", RSILoopStart)
    #print("RSI Loop End 1", RSILoopEnd)

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

    amdHistoryLastFourteenDays = amd.history(start = RSILoopStart, end = RSILoopEnd, interval="1d", actions=False)

    percentGain = 0
    percentLoss = 0
    for z in range(1, 15):
        priceDifference = amdHistoryLastFourteenDays.Close[z] - amdHistoryLastFourteenDays.Close[z-1]
        
        if(priceDifference > 0):
            percentGain += (priceDifference / amdHistoryLastFourteenDays.Close[z-1])*100
            
        if(priceDifference < 0):
            percentLoss += (priceDifference / amdHistoryLastFourteenDays.Close[z-1])*100

    averagePercentGain = percentGain / 14
    averagePercentLoss = (percentLoss / 14) * -1
            
    relativeStrength = averagePercentGain / averagePercentLoss

    #Need to calculate smoothed RSI
    relativeStrengthIndex = 100 - (100 / (1 + relativeStrength))

    #Implement MACD

    #print("Average Percent Gain", averagePercentGain)
    #print("Average Percent Loss", averagePercentLoss)
    #print("Relative Strength", relativeStrength)
    #print("Relative Strength Index", relativeStrengthIndex)

#--------------------------------------------------------------------------------------------------------------------

def main():
    start = time.time()
    stock = "AMD"
    perMinuteFundamentals(stock)
    perDayFundamentals(stock)
    end = time.time()
    print("Time Taken", end-start)

#--------------------------------------------------------------------------------------------------------------------

main()