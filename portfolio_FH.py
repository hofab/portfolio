#!/usr/bin/env python3

import yfinance as yf
import collections, functools, operator
import time



def main():
    # @todo: check for internet connection before sending of the requests
    # @todo have this as xml input and therefore agnostic

    # example portfolio
    portfolio = [
            {'name': 'TSLA', 'amount': 5, 'book': 159.128}
            ]


    getMarketData(portfolio)
    getCurrencyOfTickers(portfolio)
    calculatePercentageChanges(portfolio)
    book_value = getTotalBookValue(portfolio)
    market_value = getTotalMarketValue(portfolio)
    printDict(portfolio)
    print("===========")
    print("PORTFOLIO: " + f"{(((market_value/book_value)*100)-100):.2f}")


    exit()
def printDict(dict):
    for entry in dict:
        print(entry)

def getTickerInfo(ticker_name):
    data = yf.Ticker(ticker_name)
    return data.info

def getCurrencyConversion():
    data = yf.Ticker("CAD=X")
    info = data.info
    return info['regularMarketPrice']

def getCurrencyOfTickers(tickers):
    for ticker in tickers:
        info = getTickerInfo(ticker['name'])
        if 'currency' in info:
            ticker['currency'] = info['currency']
        else:
            ticker['currency'] = 'CAD'

def calculatePercentageChanges(tickers):
    for entry in tickers:
        if entry['market'] != [] and entry['book'] != []:
            entry['%'] = f"{((entry['market']/entry['book']*100)-100):.2f}"
        else:
            print(entry)

def testTickers(tickers):
    ticker_string = ''
    for entry in tickers:
        # last space is incorrect but yf does not care about white space at the end
        ticker_string += entry['name'] + " "

    for ticker in tickers:
        info = getTickerInfo(ticker['name'])
        ticker['market'] = info['regularMarketPrice']

# need to use same currency otherwise we are getting an error
# probably need to use info again to check what currency to use
# we will also need to get the exchange rate
def getTotalBookValue(tickers):
    total_book_value = 0

    conversion_cadusd = getCurrencyConversion()

    for entry in tickers:
        if entry['currency'] == 'USD':
            total_book_value += entry['book'] * entry['amount'] * conversion_cadusd
        else:
            total_book_value += entry['book'] * entry['amount']

    return total_book_value

# need to use same currency otherwise we are getting an error
def getTotalMarketValue(tickers):
    total_market_value = 0
    conversion_cadusd = getCurrencyConversion()
    for entry in tickers:
        if entry['currency'] == 'USD':
            total_market_value += entry['market'] * entry['amount'] * conversion_cadusd
        else:
            total_market_value += entry['market'] * entry['amount']

    return total_market_value

def getMarketData(tickers):

    info = {}
    ticker_string = ''

    for entry in tickers:
        # last space is incorrect but yf does not care about white space at the end
        ticker_string += entry['name'] + " "

    for ticker in tickers:
        ticker['market'] = []
        while ticker['market'] == []:
            info = getTickerInfo(ticker['name'])
            if info.get("regularMarketPrice") is not None:
                ticker['market'] = info['regularMarketPrice']

if __name__ == "__main__":
    main()
