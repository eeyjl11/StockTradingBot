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

def perMinute(ticker):
    today = datetime.datetime.today().replace(second = 0, microsecond = 0)

    #twoHundredMinutes = datetime.timedelta(minutes=200)
    #todayMinus = today - twoHundredMinutes
    
    #print("Today", today)
    #print("Today minus 200", todayMinus)

    #Open, High, Low, Close, Volume
    tickerHistoryPerMinute =  ticker.history(period = "202m", interval="1m", actions=False)
 
    #print("Per minute", tickerHistoryPerMinute)
    #print("First", tickerHistoryPerMinute.Close[0])
    #print("Last", tickerHistoryPerMinute.Close[200])

    tickerHistoryLength = len(tickerHistoryPerMinute)
    
    print("Length", tickerHistoryLength)

    #openArray = np.zeros(shape=(tickerHistoryLength, 1))

    #for x in range(201):
        #openArray[x, 0] = tickerHistoryPerMinute.Close[x]
        
    #tickerHistoryPerMinuteVolume = tickerHistoryPerMinute.Volume[200]
    
    #upper bollinger band = sma + (2 * standard deviation)
    #lower bollinger band = sma - (2 * standard deviation)
            
    calculatedFastMA = 0
    calculatedMediumMA = 0
    calculatedSlowMA = 0
    
    #Could consolidate into one loop with if statements
    
    #Calculate fast period moving averages
    fastEAMultiplier = 2/(20+1)
    fastEAInitialValue = tickerHistoryPerMinute.Close[180]
    
    for fastPeriod in range(20):
        calculatedFastMA += tickerHistoryPerMinute.Close[200 - fastPeriod]
        
        if(fastPeriod == 0):
            calculatedFastEA = (tickerHistoryPerMinute.Close[181] * fastEAMultiplier) + (fastEAInitialValue * (1 - fastEAMultiplier))
        else:
            calculatedFastEA = (tickerHistoryPerMinute.Close[181 + fastPeriod] * fastEAMultiplier) + (previousFastEA * (1 - fastEAMultiplier))
              
        previousFastEA = calculatedFastEA
        
    calculatedFastMA = calculatedFastMA / 20
            
    #Calculate medium period moving averages
    mediumEAMultiplier = 2/(50+1)
    mediumEAInitialValue = tickerHistoryPerMinute.Close[150]
    
    for mediumPeriod in range(50):
        calculatedMediumMA += tickerHistoryPerMinute.Close[200 - mediumPeriod]
        
        if(mediumPeriod == 0):
            calculatedMediumEA = (tickerHistoryPerMinute.Close[151] * mediumEAMultiplier) + (mediumEAInitialValue * (1 - mediumEAMultiplier))
        else:
            calculatedMediumEA = (tickerHistoryPerMinute.Close[151 + mediumPeriod] * mediumEAMultiplier) + (previousMediumEA * (1 - mediumEAMultiplier))
              
        previousMediumEA = calculatedMediumEA
        
    calculatedMediumMA = calculatedMediumMA / 50
         
    #Calculate slow period moving averages  
    slowEAMultiplier = 2/(200+1)
    slowEAInitialValue = tickerHistoryPerMinute.Close[0]
    
    for slowPeriod in range(200):
        calculatedSlowMA += tickerHistoryPerMinute.Close[200 - slowPeriod]
           
        if(slowPeriod == 0):
            calculatedSlowEA = (tickerHistoryPerMinute.Close[1] * slowEAMultiplier) + (slowEAInitialValue * (1 - slowEAMultiplier))
        else:
            calculatedSlowEA = (tickerHistoryPerMinute.Close[1 + slowPeriod] * slowEAMultiplier) + (previousSlowEA * (1 - slowEAMultiplier))
              
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
    
    perDayTicker = ticker.history(start = perDayLoopStart, end = perDayLoopEnd, interval="1d", actions=False)
    
    length = len(perDayTicker)
    
    print("Length", length)
    
    totalGain = 0
    totalLoss = 0
    
    for z in range(0, 14):
        priceDifference = perDayTicker.Close[z + 1] - perDayTicker.Close[z] #14 - 13
        
        if(priceDifference > 0):
            totalGain += priceDifference
            
        if(priceDifference < 0):
            totalLoss += priceDifference
            
    averageGain = totalGain / 14
    averageLoss = (totalLoss / 14) * -1
            
    for x in range(14, 114):
        smoothedPriceDifference = perDayTicker.Close[x + 1] - perDayTicker.Close[x] #15 - 14
        
        if(smoothedPriceDifference > 0):
            averageGain = ((averageGain * 13) + smoothedPriceDifference) / 14
            averageLoss = (averageLoss * 13)  / 14
            
        if(smoothedPriceDifference < 0):
            averageLoss = ((averageLoss * 13) + (smoothedPriceDifference * -1)) / 14
            averageGain = (averageGain * 13) / 14
            
    relativeStrength = averageGain / averageLoss

    relativeStrengthIndex = 100 - (100 / (1 + relativeStrength))
    
    print("Relative Strength Index", relativeStrengthIndex)

    calculatedTwelvePeriodEA = 0
    twelvePeriodEAMultiplier = 2/(12+1)
    previousTwelvePeriodEA = 0
    twelvePeriodSMAInitialValue = 0
    
    for twelvePeriodSMAPeriod in range(12):
        twelvePeriodSMAInitialValue += perDayTicker.Close[91 + twelvePeriodSMAPeriod]
        
    twelvePeriodSMAInitialValue = twelvePeriodSMAInitialValue / 12
        
    for twelvePeriodEAPeriod in range(12):
        if(twelvePeriodEAPeriod == 0):
            calculatedTwelvePeriodEA = (perDayTicker.Close[103] * twelvePeriodEAMultiplier) + (twelvePeriodSMAInitialValue * (1 - twelvePeriodEAMultiplier))
        else:
            calculatedTwelvePeriodEA = (perDayTicker.Close[103 + twelvePeriodEAPeriod] * twelvePeriodEAMultiplier) + (previousTwelvePeriodEA * (1 - twelvePeriodEAMultiplier))
              
        previousTwelvePeriodEA = calculatedTwelvePeriodEA
        
    calculatedTwentySixPeriodEA = 0
    twentySixPeriodEAMultiplier = 2/(26+1)
    previousTwentySixPeriodEA = 0
    twentySixPeriodSMAInitialValue = 0
    
    for twentySixPeriodSMAPeriod in range(26):
        twentySixPeriodSMAInitialValue += perDayTicker.Close[63 + twentySixPeriodSMAPeriod]
        
    twentySixPeriodSMAInitialValue = twentySixPeriodSMAInitialValue / 26
    
    for twentySixPeriodEAPeriod in range(26):
        if(twentySixPeriodEAPeriod == 0):
            calculatedTwentySixPeriodEA = (perDayTicker.Close[89] * twentySixPeriodEAMultiplier) + (twentySixPeriodSMAInitialValue * (1 - twentySixPeriodEAMultiplier))
        else:
            calculatedTwentySixPeriodEA = (perDayTicker.Close[89 + twentySixPeriodEAPeriod] * twentySixPeriodEAMultiplier) + (previousTwentySixPeriodEA * (1 - twentySixPeriodEAMultiplier))
              
        previousTwentySixPeriodEA = calculatedTwentySixPeriodEA
        
    MACD = calculatedTwelvePeriodEA - calculatedTwentySixPeriodEA
        
    #print("Twelve Period EA", calculatedTwelvePeriodEA)
    #print("Twenty Six Period EA", calculatedTwentySixPeriodEA)
    print("MACD", MACD)

#--------------------------------------------------------------------------------------------------------------------

def main():
    #need to add scheduling so perDay is called each day
    #only called on valid trading days (use pandas_market_calendars)
    
    start_time = time.time()
    stock = "AMD" 
    ticker = yf.Ticker(stock)
    perMinute(ticker)
    perDay(ticker)
    print ("Took", time.time() - start_time, "seconds to run")

#--------------------------------------------------------------------------------------------------------------------

#def populateDatabase(stock):
    #check if database for ticker exists
        #if not, create and populate with historical data from 2000?

    #check if database is up to date
        #if not populate with missing values

#--------------------------------------------------------------------------------------------------------------------

main()