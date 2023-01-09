#!/usr/bin/env python3

import yfinance as yf
import collections, functools, operator
import time
import requests
import yaml

# check for internet connection before sending of the requests

def main():
    check_internet_connection()
    # portfolio = read_in_portfolio_from_file('my_portfolio.yaml')
    # print(portfolio)
    # getMarketData(portfolio['portfolio'])
    # exit()

    print(ticker_tfsa)

    s = time.strftime("%c")
    print(s)

    getMarketData(ticker_rrsp)
    calculatePercentageChanges(ticker_rrsp)
    book_value = getTotalBookValue(ticker_rrsp)
    market_value = getTotalMarketValue(ticker_rrsp)
    printDict(ticker_rrsp)
    print("===========")
    print("RRSP: " + f"{(((market_value/book_value)*100)-100):.2f}")

    getMarketData(ticker_tfsa)
    # getCurrencyOfTickers(ticker_tfsa)
    calculatePercentageChanges(ticker_tfsa)
    book_value = getTotalBookValue(ticker_tfsa)
    market_value = getTotalMarketValue(ticker_tfsa)
    printDict(ticker_tfsa)
    print("===========")
    print("TFSA: " + f"{(((market_value/book_value)*100)-100):.2f}")

    getMarketData(tfsa)
    # getCurrencyOfTickers(tfsa)
    calculatePercentageChanges(tfsa)
    conversion_cadusd = getCurrencyConversion()
    book_value = getTotalBookValue(tfsa)
    printDict(tfsa)
    for entry in tfsa:
        if entry['Currency'] == 'USD':
            entry['book'] = entry['book'] / conversion_cadusd

    book_value = getTotalBookValue(tfsa)
    market_value = getTotalMarketValue(tfsa)
    print("===========")
    print("TFSA (D): " + f"{(((market_value/book_value)*100)-100):.2f}")
    print("TFSA (D): " + "Book Value:" +f"{book_value:.2f}")
    print("TFSA (D): " + "Market Value:" +f"{market_value:.2f}")

    exit()

def read_in_portfolio_from_file(filename):
    with open(filename, 'r') as file:
        portfolio = yaml.safe_load(file)
        return portfolio

def check_internet_connection():
    try:
        requests.head("https://www.startpage.com/", timeout=5)
    except reqeusts.ConnectionError:
        print("No internet connection - check network")

def printDict(dict):
    for entry in dict:
        print(entry)

def getTickerInfo(ticker_name):
    print(ticker_name)
    data = yf.Ticker(ticker_name)
    print(data.info)
    return data.info

def getOneDayHistory(ticker_name):
    data = yf.Ticker(ticker_name)
    todays_data = data.history(period='1d')
    return todays_data

def getCurrencyConversion():
    data = yf.Ticker("CAD=X")
    todays_data = data.history(period='1d')
    return todays_data['Close'][-1]

# def getCurrencyOfTickers(tickers):
#     for ticker in tickers:
#         today_data = getOneDayHistory(ticker['name'])
#         if 'currency' in today_data['Close'][-1]:
#             ticker['currency'] = today_data['Close'][-1]
#         else:
#             ticker['currency'] = 'CAD'

def calculatePercentageChanges(tickers):
    for entry in tickers:
        if entry['market'] and entry['book']:
            entry['%'] = f"{((entry['market']/entry['book']*100)-100):.2f}"
        else:
            print(entry)

def testTickers(tickers):
    ticker_string = ''
    for entry in tickers:
        # last space is incorrect but yf does not care about white space at the end
        ticker_string += entry['name'] + " "

    for ticker in tickers:
        ticker.info
        info = getTickerInfo(ticker['name'])
        ticker['market'] = info['regularMarketPrice']

# need to use same currency otherwise we are getting an error
# probably need to use info again to check what currency to use
# we will also need to get the exchange rate
def getTotalBookValue(tickers):
    total_book_value = 0

    conversion_cadusd = getCurrencyConversion()

    for entry in tickers:
        if entry['Currency'] == 'USD':
            total_book_value += entry['book'] * entry['amount'] * conversion_cadusd
        else:
            total_book_value += entry['book'] * entry['amount']

    return total_book_value

# need to use same currency otherwise we are getting an error
def getTotalMarketValue(tickers):
    total_market_value = 0
    conversion_cadusd = getCurrencyConversion()
    for entry in tickers:
        if entry['Currency'] == 'USD':
            total_market_value += entry['market'] * entry['amount'] * conversion_cadusd
        else:
            total_market_value += entry['market'] * entry['amount']

    return total_market_value

def getMarketData(tickers):

    ticker_string = ''

    for entry in tickers:
        # last space is incorrect but yf does not care about white space at the end
        ticker_string += entry['name'] + " "

    for ticker in tickers:
        ticker['market'] = []
        while not ticker['market']:
            todays_data = getOneDayHistory(ticker['name'])
            if todays_data['Close'][-1]:
                ticker['market'] = todays_data['Close'][-1]

if __name__ == "__main__":
    main()
