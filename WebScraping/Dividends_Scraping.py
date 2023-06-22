import pandas as pd

from pymongo import MongoClient
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict


# MongoDB connection details
uri = "mongodb+srv://peterminbashian:Kirby123@cluster0.pwcghtt.mongodb.net/?retryWrites=true&w=majority"
database_name = "STOCKS"
collection_name = "DIV_INFO"

# holdings = [
#     "RY",   # Royal Bank of Canada
#     "TD",   # Toronto-Dominion Bank
#     "BNS",  # Bank of Nova Scotia
#     "CNR",  # Canadian National Railway Company
#     "ENB",  # Enbridge Inc.
#     "SU",   # Suncor Energy Inc.
#     "ABX",  # Barrick Gold Corporation
#     "CM",   # Canadian Imperial Bank of Commerce
#     "BAM.A",    # Brookfield Asset Management Inc.
#     "CNQ",  # Canadian Natural Resources Limited
#     # Add more ticker symbols...
# ]

holdings = []

# tickers = open('Tickers.txt', 'r')
# Read the CSV file into a DataFrame
stocksdf = pd.read_csv('/Users/peterminbashian/Projects/DividendCompounder/WebScraping/companiesmarketcap.com - Largest American companies by market capitalization.csv')


# Extract a single column
tickers = stocksdf['Symbol']


for ticker in tickers:
    holdings.append(ticker[:-1])

# Create a new client and connect to the server
client = MongoClient(uri)
flag = 0

dividends = defaultdict(list)
df = pd.DataFrame(columns=['ticker', 'ex_dividend_date', 'payment_date', 'amount'])

for ticker in holdings:
    data = defaultdict(list)
    url = f"https://dividendhistory.org/payout/TSX/{ticker}/"
    # url = f"https://dividendhistory.org/payout/{ticker}/"
    try:
        page = urlopen(url)
    except Exception as e:
        print(f"Error retrieving info on: {ticker}")
        continue
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    start_index = html.find("<table id='dividend_table' class='table table-striped table-bordered'>")
    end_index = html.find("</tr></tbody></table>")
    table = html[start_index:end_index]
    table = table[table.find('<tbody>'):table.find('</tbody>')]
    soup = BeautifulSoup(table, 'html.parser')
    trs = soup.find_all('tr')
    
    for tr in trs:
        tds = tr.find_all('td')
        lineNumber = 0
        dividend_data={}
        for td in tds:
            if lineNumber == 0:
                dividend_data['ticker']=ticker
                dividend_data['ex_dividend_date']=(td.text.strip())
            elif lineNumber == 1:
                dividend_data['payment_date']=(td.text.strip())
            elif lineNumber == 2:
                dividend_data['amount']=(td.text.strip())
            lineNumber+=1
            # print(dividend_data)
            # exit()

        df.loc[len(df)] = dividend_data
    # df.to_csv('Database/Canadian_Company_Dividends.csv', index=False)
            # print('Appended')
    # df = df.append(pd.DataFrame(dividend_data))

df.to_csv('Database/US_Company_Dividends.csv', index=False)
# db = client[database_name]
# collection = db[collection_name]

# result = collection.insert_one({Dividends: data})

# # Check the insertion result
# if result.acknowledged:
#     print("Documents inserted successfully. Inserted IDs")
# else:
#     print("Documents insertion failed.")