import time
import csv
from io import StringIO
import ssl
import json
from urllib.request import urlopen
from datetime import datetime, timedelta


# Get current time in seconds since the Unix Epoch
end_time = int(time.time())
# Get time 24 hours ago
start_time = end_time - 60*60*24*8
symbol="GC=F"
print("Symbol:", symbol)

def process_data(data):
    # Remove the first row (headers)
    data = data[1:]

    # Use a dictionary to store the rows, using the date as the key
    # If a date is repeated, the later row will overwrite the earlier one
    data_dict = {row[0]: row for row in data}

    # Convert the dictionary back into a list of lists
    processed_data = list(data_dict.values())

    # Find the range of dates in the data
    dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in processed_data]
    start_date = min(dates)
    end_date = max(dates)

    # Create a new dictionary with a continuous range of dates
    current_date = start_date
    final = {}
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        if date_str in data_dict:
            # Use the closing price if the date exists in the data
            final[date_str] = data_dict[date_str][4]
        else:
            # Use 'No Data' if the date does not exist in the data
            final[date_str] = 'No Data'
        current_date += timedelta(days=1)
    
    return final


def get_stocks_data( symbol: str):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_time}&period2={end_time}&interval=1d&events=history&includeAdjustedClose=true".format(symbol=symbol)
        data = {}
        ssl._create_default_https_context = ssl._create_unverified_context
        with urlopen(url, timeout=10) as connection:
            res = connection.read().decode()
            _ = csv.reader(StringIO(res))
            cleaned = process_data(list(_))
            return cleaned
    except Exception as e:
        print("error on get_stocks_data:",e)
        # bad url, socket timeout, http forbidden, etc.
        return None

data = get_stocks_data("GC=F") 
print("test",data)
# for row in data:
#     print(row)
