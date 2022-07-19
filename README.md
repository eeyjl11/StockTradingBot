# StockTradingBot

A stock trading bot that uses a machine learning algorithm to buy and sell stocks.

## Description

The bot uses a list of strings which contains the tickers of the stock you wish to trade. It creates a database file for each stock containing the calculated technical indicators. The machine learning model is then trained and backtested on this data. It then trades real stocks using the trader class.

## Required libraries:
- Yfinance
- Pandas
- Numpy
- Matplotlib
- Datetime
- Schedule
