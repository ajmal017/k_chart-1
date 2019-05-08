# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:03:23 2019

@author: w
"""
import os
import pandas as pd

# Read data from CSV files
def read_csv(etf_tickers, end_date):    
    pl = None    
    for e in etf_tickers:
        # Read
        csv_path = os.getcwd() + "\\Data\\"
        csv_filename = csv_path + e + end_date + '.csv'
        df = pd.read_csv(csv_filename)
        p_t=['Date','Adj Close']
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