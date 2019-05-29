# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:03:23 2019

@author: w
"""
import os
import pandas as pd
from eod_historical_data import get_eod_data

# Read data from CSV files
def read_csv(etf_tickers, end_date=''):    
    pl = None    
    p_t=['Date','Adj Close']
    for e in etf_tickers:
        # Read
        csv_path = os.getcwd() + "\\Data\\"
        csv_filename = csv_path + e + end_date + '.csv'
        df = pd.read_csv(csv_filename)
        p=df[p_t].sort_values(by='Date')
        p['Date'] = pd.to_datetime(p['Date'])
        p.set_index("Date", inplace=True)
        p = p.rename({'Adj Close':e}, axis=1)        
        # Merge
        if pl is None:
            pl=p
        else:
            pl = pd.merge(pl,p,left_index=True, right_index=True)        
    return pl

# Download data from eodhistoricaldata.com
def read_eod(tickers, market='US'):
    api_token = '5cebe613e02010.08022109'
    pl = None
    p_t=['Adjusted_close']
    for e in tickers:
        df = get_eod_data(e, market, None, None, api_token, None)
        p = df[p_t]
        p = p.rename({'Adjusted_close':e}, axis=1)
        if pl is None:
            pl=p
        else:
            pl = pd.merge(pl,p,left_index=True, right_index=True)
    return pl

def save_eod(tickers, market='US'):
    api_token = '5cebe613e02010.08022109'
    csv_path = os.getcwd() + "\\Data\\"
    for e in tickers:
        df = get_eod_data(e, market, None, None, api_token, None)
        df = df.rename({'Adjusted_close':'Adj Close'}, axis=1)
        csv_filename = csv_path + e + '.csv'
        df.to_csv(csv_filename, encoding='utf-8')
        
        