# -*- coding: utf-8 -*-
"""
Created on Mon May  6 09:52:25 2019

@author: w
"""

import requests
import pandas as pd
from pandas.compat import StringIO
import json

# https://eodhistoricaldata.com/api/eod/AAPL.US?api_token={your_api_key}
def get_historical_data(symbol="AAPL.US", api_token="5cebe613e02010.08022109", session=None):
    if session is None:
        session = requests.Session()        
        url = "https://eodhistoricaldata.com/api/eod/%s" % symbol        
        params = {        
            "api_token": api_token        
        }
        r = session.get(url, params=params)
        if r.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine="python")
        return df
    else:
        raise Exception(r.status_code, r.reason, url)

# https://eodhistoricaldata.com/api/fundamentals/AAPL.US?api_token={your_api_key}        
def get_fundamental_data(symbol="AAPL.US", api_token="5cebe613e02010.08022109", session=None):
    if session is None:
        session = requests.Session()        
        url = "https://eodhistoricaldata.com/api/fundamentals/%s" % symbol        
        params = {        
            "api_token": api_token        
        }
        r = session.get(url, params=params)
        if r.status_code == requests.codes.ok:
            j = json.load(StringIO(r.text))
        return j
    else:
        raise Exception(r.status_code, r.reason, url)

# https://eodhistoricaldata.com/api/real-time/AAPL.US?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX&fmt=json
def get_realtime_data(symbol="AAPL.US", api_token="5cebe613e02010.08022109", session=None):
    if session is None:
        session = requests.Session()        
        url = "https://eodhistoricaldata.com/api/real-time/%s" % symbol        
        params = {        
            "api_token": api_token        
        }
        r = session.get(url, params=params)
        if r.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine="python")
        return df
    else:
        raise Exception(r.status_code, r.reason, url)


# read historical data
ticker = 'SHY.US'
ticker = 'HSI.INDX'
ticker = '0700.HK'
df = get_historical_data(ticker)
for e in df.columns:
    print(e, df[e][-1])
#print(df.tail())

'''
# read real time data
ticker = 'HSI.INDX'
ticker = '0700.HK'
#df = get_historical_data(ticker)
df = get_realtime_data(ticker)
for e in df.columns:
    print(e, df[e][-1])
#print(df.tail())

'''
# read fundamental data
# save to json file
ticker = '2833.HK' # HSI ETF
ticker = '0700.HK' # Tencent
fd = get_fundamental_data(ticker)
print(json.dumps(fd, indent=4, sort_keys=True))
json_file = ticker + '.json'
with open(json_file, 'w') as f:
    json.dump(fd, f, indent=4, sort_keys=True)
    
'''
# get index constituents
ticker = 'GSPC.INDX'
index = get_fundamental_data(ticker)
print(json.dumps(index, indent=4, sort_keys=True))
json_file = ticker + '.json'
with open(json_file, 'w') as f:
    json.dump(fd, f, indent=4, sort_keys=True)
'''