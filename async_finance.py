import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from datetime import datetime
from io import StringIO
import csv
import json
from urllib.request import urlopen
import ssl
from ticker_data import TickerData
from datetime import datetime, timedelta

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
            final[date_str] = "nodata"
        current_date += timedelta(days=1)
    
    return final


class Finance(object):
    """Object dedicated to update the stocks_data.json file with fresh numbers from the API"""
    def __init__(self):
        self.tickerData = TickerData()
        self.thread = Thread(target=self.run_yfinance)
        self.thread.daemon = True
        self.thread.start()
        # self.thread.join()

    def get_stocks_data(self, ticker):
        # set time range for query for the last days
        days = 8
        end_time = int(time.time())
        start_time = end_time - 60*60*24*days
        symbol = ticker["symbol"]
        try:
            url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_time}&period2={end_time}&interval=1d&events=history&includeAdjustedClose=true".format(symbol=symbol)
            data = {}
            ssl._create_default_https_context = ssl._create_unverified_context
            with urlopen(url, timeout=10) as connection:
                res = connection.read().decode()
                _ = csv.reader(StringIO(res))
                cleaned = process_data(list(_))
                data[symbol] = cleaned
                return data
        except Exception as e:
            print("Problem getting data from Yahoo Finance:",e)
            # bad url, socket timeout, http forbidden, etc.
            return None

    def save_file(self,dict_data):
        with open('stock_data.json', 'w') as file:
            json.dump(dict_data, file)    

    def run_yfinance(self):
        tickers = self.tickerData.tickers["tickers"]
        while True:
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = pool.map(self.get_stocks_data, tickers)
            data = {}
            try:
                for r in results:
                    if r is not None:  # only update data if response is not None
                        data.update(r)
                if len(data) == len(tickers):  # only save to file if data for all tickers is available
                    try:
                        self.save_file(data)
                        print("Updated stock_data.json at", datetime.now())
                    except Exception as e: 
                        print("Error while saving stock data to file:", e)  
            except Exception as e: 
                print("ERROR async_finance.py, problem getting data from Yahoo Finance:", e)
            time.sleep(3600) # check for new values every hour