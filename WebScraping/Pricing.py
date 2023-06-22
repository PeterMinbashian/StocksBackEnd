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
i = 0

while i < len(tickers):
    data = defaultdict(list)
    ticker = tickers[i]
    if ticker in df['ticker']:
        i += 1
        continue
    url = f"https://www.google.com/finance/quote/{ticker}:{exchanges[exchangeIndex]}?hl=en"
    try:
        page = urlopen(url)
    except Exception as e:
        print(f"Error retrieving info on: {ticker}")
        print(e)
        continue
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    price = soup.find('div', class_="kf1m0")
    
    try:
        price = price.text.strip().replace("$","")
    except Exception as e:
        exchangeIndex += 1
        if exchangeIndex > 2:
            print(f'Retrevied NULL value From: {ticker}')
            exchangeIndex = 0
            i += 1
            continue
        else:
            continue
    pricing = {'ticker': ticker, 'price':price, 'exchange': exchanges[exchangeIndex]}
    df.loc[len(df)] = pricing
    i += 1
    exchangeIndex = 0

df.to_csv('Database/Stocks.csv', index=False)
