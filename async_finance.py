import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from datetime import datetime, timedelta
from io import StringIO
import csv
import json
import yfinance as yf
from ticker_data import TickerData


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
        # Set time range for query for the last 8 days
        days = 8
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        symbol = ticker["symbol"]

        try:
            data = {}
            ticker_yf = yf.Ticker(symbol)
            hist = ticker_yf.history(start=start_date, end=end_date, interval="1d")

            # Convert the history data to a list of lists as expected by process_data
            hist_list = [["Date", "Open", "High", "Low", "Close", "Volume"]]
            for date, row in hist.iterrows():
                hist_list.append([date.strftime('%Y-%m-%d'), row["Open"], row["High"], row["Low"], row["Close"], row["Volume"]])

            cleaned = process_data(hist_list)
            data[symbol] = cleaned
            return data
        except Exception as e:
            print("Problem getting data from Yahoo Finance:", e)
            return None

    def save_file(self, dict_data):
        try:
            with open('stock_data.json', 'w') as file:
                json.dump(dict_data, file)
        except Exception as e:
            print("Error while saving stock data to file:", e)

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
            time.sleep(86400)  # sleep for one day

# Example usage
if __name__ == "__main__":
    finance = Finance()
    finance.thread.join()  # This will keep the main thread running
