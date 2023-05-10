#!/usr/bin/env python
import json
class TickerData(object):
    def __init__(self):
        with open('tickers.json') as f:
            self.tickers = json.load(f)

    def symbols_list(self):
        list =[]
        for ticker in self.tickers['tickers']:
            list.append(ticker['symbol'])
        return list
