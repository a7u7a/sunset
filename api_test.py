import time
import requests
import csv
from io import StringIO
import ssl
import json
from urllib.request import urlopen

# Get current time in seconds since the Unix Epoch
end_time = int(time.time())
# Get time 24 hours ago
start_time = end_time - 60*60*24*8
symbol="HG=F"
print("Symbol:", symbol)

def get_stocks_data( symbol: str):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_time}&period2={end_time}&interval=1d&events=history&includeAdjustedClose=true".format(symbol=symbol)
        data = {}
        ssl._create_default_https_context = ssl._create_unverified_context
        with urlopen(url, timeout=10) as connection:
            res = connection.read().decode()
            csv_data = csv.reader(StringIO(res))
            return csv_data
    except Exception as e:
        print("error on get_stocks_data:",e)
        # bad url, socket timeout, http forbidden, etc.
        return None

data = get_stocks_data("GC=F") 
for row in data:
    print(row)
