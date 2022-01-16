import pandas as pd
from pandas.tseries.offsets import BDay
import pandas_market_calendars as mcal
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as datetime
import time

start = time.time()

amd = yf.Ticker("AMD")

today = datetime.datetime.today()
RSILoopStart = (today - BDay(15))
RSILoopEnd = (today - BDay(1))

twelvePeriodEMA = 0
twentySixPeriodEMA  = 0

print("RSI Loop Start 1", RSILoopStart)
print("RSI Loop End 1", RSILoopEnd)

nyse = mcal.get_calendar('NYSE')
nyseValidDays = nyse.valid_days(start_date=RSILoopStart, end_date=RSILoopEnd)

print("NYSE Working Days", nyseValidDays)

#for p in range(len(nyseValidDays)):
    #If Statements not working
    #Needs to check if date is in valid days
    #Use strftime to remove hours and minutes etc
    #if(RSILoopEnd not in nyseValidDays):
        #RSILoopStart = (RSILoopStart - BDay(1))
        #RSILoopEnd = (RSILoopEnd - BDay(1))

    #if(RSILoopStart not in nyseValidDays):
        #RSILoopStart = (RSILoopStart - BDay(1))

print("RSI Loop Start 2", RSILoopStart)
print("RSI Loop End 2", RSILoopEnd)

#Open, High, Low, Close, Volume
amdHistoryPerMinute = amd.history(period="7d", interval="1m", actions=False)
amdHistoryLastFourteenDays = amd.history(start=RSILoopStart, end = RSILoopEnd, interval="1d", actions=False)

print(amdHistoryLastFourteenDays)

amdHistoryLength = len(amdHistoryPerMinute)

openArray = np.zeros(shape=(amdHistoryLength, 5))
twoHundredMinuteArray = np.zeros(shape=(200, 1))

calculatedFastMA = 0
calculatedMediumMA = 0
calculatedSlowMA = 0

for x in range(amdHistoryLength):
    openArray[x, 0] = amdHistoryPerMinute.Open[x]
    openArray[x, 1] = amdHistoryPerMinute.High[x]
    openArray[x, 2] = amdHistoryPerMinute.Low[x]
    openArray[x, 3] = amdHistoryPerMinute.Close[x]
    openArray[x, 4] = amdHistoryPerMinute.Volume[x]
    
    #Calculate the EMA too
    for y in range(0,199):
        twoHundredMinuteArray[199-y] = twoHundredMinuteArray[198-y]
        
    twoHundredMinuteArray[0] = amdHistoryPerMinute.Close[x]
        
    for fastPeriod in range(20):
        calculatedFastMA += twoHundredMinuteArray[fastPeriod]
    
    calculatedFastMA = calculatedFastMA / 20
        
    for mediumPeriod in range(50):
        calculatedMediumMA += twoHundredMinuteArray[mediumPeriod]
    
    calculatedMediumMA = calculatedMediumMA / 50 
        
    for slowPeriod in range(200):
        calculatedSlowMA += twoHundredMinuteArray[slowPeriod]
    
    calculatedSlowMA = calculatedSlowMA / 200
    
    if 0 in openArray[x]:
        openArray[x] = 0

percentGain = 0
percentLoss = 0
for z in range(1, 15):
    priceDifference = amdHistoryLastFourteenDays.Close[z] - amdHistoryLastFourteenDays.Close[z-1]
    #print("Price Difference", priceDifference)
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

end = time.time()

print("Average Percent Gain", averagePercentGain)
print("Average Percent Loss", averagePercentLoss)
print("Relative Strength", relativeStrength)
print("Relative Strength Index", relativeStrengthIndex)
print("Fast Moving Average", calculatedFastMA)
print("Medium Moving Average", calculatedMediumMA)
print("Slow Moving Average", calculatedSlowMA)
print("Time Taken", end-start)

#for Datetime in amdHistory.index:
    #timeData = amdHistory[Datetime: Datetime]
    #print(amdHistory.loc[[Datetime], ["Open"]])