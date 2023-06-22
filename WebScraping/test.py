import pyodbc

# Azure SQL Server credentials
server = 'your_server.database.windows.net'
database = 'Stocks'
username = 'peterminbashian'
password = 'Kirby123!'
driver = '{ODBC Driver 18 for SQL Server}'  # Make sure the appropriate driver is installed

# Establishing the connection
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(conn_str)

# Creating a cursor object
cursor = conn.cursor()
exit()

# Executing a sample query
cursor.execute("SELECT * FROM your_table")

# Fetching and printing the results
for row in cursor.fetchall():
    print(row)

# Closing the connection
cursor.close()
conn.close()