import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict


companies = pd.read_csv('companiesmarketcap.com - Largest American companies by market capitalization.csv')
names = companies['Name'].tolist()
tickers = companies['Symbol'].tolist()

names = [string.split(' ')[0] for string in names]
df = pd.DataFrame(columns=['Ticker', 'Date', 'Price', 'EPS'])
for name, ticker in zip(names, tickers):
    tempDict = {}
    try:
        url = f"https://www.macrotrends.net/stocks/charts/{ticker}/{name}/pe-ratio"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        trs = table.find_all('tr')
        trs = trs[2:]
        for tr in trs:
            tds = tr.find_all('td')
            tempDict = {'Ticker': ticker, 'Date': tds[0].text.strip(), 'Price': tds[1].text.strip(), 'EPS': tds[2].text.strip()}
            df.loc[len(df)] = tempDict
        
    except Exception as e:
        print('ERROR WITH ', name, ticker)
        continue
    print(f'ADDED {name}')
df.to_csv('Database/HistoricData')

