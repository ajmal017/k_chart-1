# -*- coding: utf-8 -*-
#########################################
# @author: YK
#
# inputs: 
# 1. weights at t+1 calc-ed based on t
# 2. transaction prices at t+1
# 3. asset historical prices
#
# outputs:
# 1. value and cash at date end
# 2. transaction results at t+1
# 3. performance results at date end
# 4. graph for values and weights
#########################################

import os
import sys
package_path = os.getcwd()
if package_path not in sys.path:
    sys.path.append(package_path)

import datetime
import pandas as pd
import numpy as np
from Reporting.placement import est_transacton_prices
from Reporting.placement import get_value
from Data.get_data import read_ticker

# 1. load historical data in a dict and key is ticker
tickers=['SHY','SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
tickers_pl = {}
for e in range(len(tickers)):
    tickers_pl[tickers[e]] = read_ticker(tickers[e])
# EXAMPLEs for dict of tickers and prices
#for k, v in tickers_pl.items():
#    print(k, v.tail())
#    print(k, tickers_pl[k].tail())

# 2. load delta_shares from file
delta_shares_name = 's.xlsx'
df = pd.read_excel(open(delta_shares_name,'rb'), sheet_name=0)
delta_s = df.copy()
delta_s.set_index("Date", inplace=True)
tickers = delta_s.columns
# EXAMPLEs for dict of tickers and prices
#for e in tickers:
#    print(e, tickers_pl[e].tail())

# 3. load transaction prices
# 3.1 scenario one: estimate transaction prices
trans_prices, shares = est_transacton_prices(tickers, delta_s, tickers_pl)
#print(trans_prices, shares)

# 4. calc new value with new trades
# shares, cash and value at t = 0 at delta_s[0]'s date
# move date by date, calc value for each date
# if reach delta_s.date, read the delta_s and wait placement
# if placement, write transaction slip and update shares, cash and value
# move date by date

# combine total shares and trans_prices

# t=0
cash = 500000
portfolio = pd.DataFrame(columns=delta_s.columns)
portfolio.loc[len(portfolio)] = np.zeros(len(tickers))
portfolio['Date'] = delta_s.index[0]
portfolio['Cash'] = cash
portfolio['Value'] = 0.0

start_date = delta_s.index[0]
end_date = tickers_pl[tickers[0]].index[-1]
t = 0
s = np.zeros(len(tickers))
for d in pd.date_range(start=start_date, end=end_date, freq='D'):
    if datetime.datetime.weekday(d)<=4:
        # calc value
        portfolio.loc[len(portfolio)] = portfolio.loc[len(portfolio)-1]
        if d == shares.index[t]:
            s = shares[tickers].iloc[t].values
            #portfolio[tickers].iloc[-1] = s
            if t < len(shares.index)-1:
                t = t + 1
        portfolio['Date'].iloc[-1] = d        
        #s = portfolio[tickers].iloc[-1].values
        portfolio['Value'].iloc[-1] = get_value(tickers, d, s, tickers_pl)
print(portfolio)
