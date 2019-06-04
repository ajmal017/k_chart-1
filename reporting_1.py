# -*- coding: utf-8 -*-
"""
Created on Thu May 30 23:12:24 2019

@author: w
"""

import os
import sys
package_path = os.getcwd()
if package_path not in sys.path:
    sys.path.append(package_path)

import pandas as pd
import numpy as np
from Reporting.placement import get_allocation, get_value, get_close_price
from Data.get_data import get_working_date
from Data.get_data import read_price

df = pd.read_excel(open('s.xlsx','rb'), sheet_name=0)
s = df.copy()
s.set_index("Date", inplace=True)

# portfolio assets
tickers = s.columns

# t=0
shares = np.zeros(len(tickers))
cash = 500000
# pre_price at t=0
t_date = s.index[0]
pre_t_date = get_working_date(t_date, True)
prices = shares.copy()
for e in range(len(tickers)):    
    c = read_price(pre_t_date, tickers[e])
    prices[e] = c.Close
value = 0.0
print(pre_t_date.strftime("%Y-%m-%d"), shares, "{0:42.2f}".format(cash), "{0:.2f}".format(value))

# t>=1
for t in range(len(s.index)):
    pre_shares = shares
    pre_cash = cash
    pre_prices = prices
    t_date = s.index[t]
    t_date = get_working_date(t_date)
    delta_s = np.zeros(len(tickers))
    for e in range(len(tickers)): 
        delta_s[e] = s[s.columns[e]][t]
    shares, cash, place_prices = get_allocation(tickers, t_date, delta_s, pre_shares, pre_cash, pre_prices)
    value = get_value(tickers, t_date, shares, cash)
    prices = get_close_price(tickers, t_date, None, True)
    #print('--- ---')
    #print(t_date.strftime("%Y-%m-%d"), place_prices)
    print(t_date.strftime("%Y-%m-%d"), shares, "{0:.2f}".format(cash), "{0:.2f}".format(value))
    