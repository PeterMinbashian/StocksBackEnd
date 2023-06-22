import pandas as pd
import numpy as np

stocks = pd.read_csv('Database/Stocks.csv')
stocks['currency'] = np.where(stocks['exchange'] == 'TSE', 'CAD', 'USA')

print(stocks)

stocks.to_csv('Database/Stocks.csv')