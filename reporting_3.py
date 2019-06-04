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

import pandas as pd
from Reporting.placement import est_transacton_prices
from Reporting.results import mapping #get_portfolio
from Data.get_data import read_ticker

# 1. load historical data in a dict and key is ticker
tickers=['SHY','SPY','XLB','XLE','XLF','XLI','XLK','XLP','XLU','XLV','XLY']
tickers_pl = {}
for e in range(len(tickers)):
    tickers_pl[tickers[e]] = read_ticker(tickers[e])

# 2. load delta_shares from file
delta_shares_name = 's.xlsx'
df = pd.read_excel(open(delta_shares_name,'rb'), sheet_name=0)
delta_s = df.copy()
delta_s.set_index("Date", inplace=True)
tickers = delta_s.columns

# 3. load transaction prices
# 3.1 scenario one: estimate transaction prices, transaction dates, shares at each t and cash at each t
init_cash = 500000
trans_dates, trans_prices, shares, residual_cashs = est_transacton_prices(tickers, delta_s, tickers_pl, init_cash)
#for t in range(len(trans_dates)):
#    print(trans_dates[t].strftime("%Y-%m-%d"), trans_prices[t], "{0:0.2f}".format(cashs[t]))

# 3.2 scenario two: input transaction prices

# 4. calc new value with new trades
# shares, cash and value at t = 0 at delta_s[0]'s date
# move date by date, calc value for each date
# if reach delta_s.date, read the delta_s and wait placement
# if placement, write transaction slip and update shares, cash and value
# move date by date
mapping_date, mapping_shares, mapping_closes, mapping_cash, mapping_value = mapping(tickers, delta_s, tickers_pl, init_cash, trans_dates, trans_prices, shares, residual_cashs)
#print(mapping_date, mapping_shares, mapping_closes, mapping_cash, mapping_value)
for t in range(len(mapping_date)):
    print(mapping_date[t].strftime("%Y-%m-%d"), \
          mapping_closes[t], \
          "{0:0.2f}".format(mapping_cash[t]), \
          "{0:0.2f}".format(mapping_value[t]))