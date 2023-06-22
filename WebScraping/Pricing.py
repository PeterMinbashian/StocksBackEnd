import pandas as pd
import time

from pymongo import MongoClient
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict

stocksUS = pd.read_csv('companiesmarketcap.com - Largest American companies by market capitalization.csv')
stocksCAD = pd.read_csv('companiesmarketcap.com - Largest Canadian companies by market capitalization.csv')

tickers = stocksUS['Symbol'].tolist() + stocksCAD['Symbol'].tolist() 

dividends = defaultdict(list)
df = pd.read_csv('Database/Stocks.csv')
exchanges = ['TSE', 'NASDAQ', 'NYSE']
exchangeIndex = 0

for i in range(len(tickers)):
    print(exchangeIndex)
    data = defaultdict(list)
    ticker = tickers[i]
    url = f"https://www.google.com/finance/quote/{ticker}:{exchanges[exchangeIndex]}?hl=en"

    if '.' in ticker:
        ticker=ticker[:ticker.index('.')]
    else:
        i += 1
        exchangeIndex = 0
        continue
    
    # url = f"https://www.marketwatch.com/investing/stock/{ticker}?countrycode=ca&mod=search_symbol"
    # url = f"https://dividendhistory.org/payout/{ticker}/"
    try:
        page = urlopen(url)
    except Exception as e:
        print(f"Error retrieving info on: {ticker}")
        print(e)
        continue
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    # start_index = html.find("<table id='dividend_table' class='table table-striped table-bordered'>")
    soup = BeautifulSoup(html, 'html.parser')
    price = soup.find('div', class_="kf1m0")
    
    try:
        price = price.text.strip().replace("$","")
    except Exception as e:
        exchangeIndex += 1
        if exchangeIndex > 2:
            print(f'Retrevied NULL value From: {ticker}')
            i += 1
            exchangeIndex = 0
            continue
        else:
            continue
    pricing = {'ticker': ticker, 'price':price, 'exchange': exchanges[exchangeIndex]}

    df.loc[len(df)] = pricing
    print('Added')
    i += 1
    exchangeIndex = 0

df.to_csv('Database/Stocks.csv', index=False)
