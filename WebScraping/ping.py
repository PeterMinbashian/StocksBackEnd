from pymongo import MongoClient

# MongoDB connection details
uri = "mongodb+srv://peterminbashian:Z6yq1pldvPlz6DtH@cluster0.pwcghtt.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the MongoDB server
client = MongoClient(uri)

# Access the desired database and collection
database = client['STOCKS']
collection = database['DIV_INFO']

# Retrieve the document
query = {'ENB': {'$exists': True}}
document = collection.find_one(query)

# Process the document
if document:
    # Document found
    print(document)
else:
    # Document not found
    print("Document not found.")

# Close the MongoDB connection
client.close()

# import pandas as pd

# from pymongo import MongoClient
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from collections import defaultdict

# url = "https://companiesmarketcap.com/canada/largest-companies-in-canada-by-market-cap/"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")

# with open('output.txt', 'r') as file:
#     content = file.read()

# soup = BeautifulSoup(content, 'html.parser')

# # Find all <a> elements with href attribute starting with "/stock/tsx-"
# a_elements = soup.find_all('a', href=lambda href: href and href.startswith("/stock/tsx-"))
# file = open('Tickers.txt', 'w')
# for a in a_elements:
#     file.write(a.text.strip() + '\n')
#     print(a.text.strip())
