# Calculates the technical indicators for each stock

import yfinance as yf

class Stock:
    def perMinute(self, date, stock):
        ticker = yf.Ticker(stock)

        #Open, High, Low, Close, Volume
        tickerHistoryPerMinute =  ticker.history(end = date, period = "202m", interval="1m", actions=False)
    
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
        
        # Calculate fast period moving averages
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
                
        # Calculate medium period moving averages
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
            
        # Calculate slow period moving averages  
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

    def perDay(self, date, stock):
        ticker = yf.Ticker(stock)

        perDayTicker = ticker.history(end = date, period = "115d", interval="1d", actions=False)
    
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