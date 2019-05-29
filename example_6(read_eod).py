# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:17:41 2019

@author: w
"""

import os
import sys
package_path = os.getcwd()
if package_path not in sys.path:
    sys.path.append(package_path)

from Data.get_data import read_eod
from Data.get_data import save_eod, read_csv
'''
etf_tickers=['SHY','SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
#pl=read_eod(etf_tickers)
#save_eod(etf_tickers)
pl=read_csv(etf_tickers)
wp = pl.resample('W', loffset=pd.offsets.timedelta(days=0)).last().dropna()
wp.to_csv('wp.csv')
'''
etf_tickers=['2833']
pl=read_eod(etf_tickers, 'HK')
print(pl.head())
print(pl.tail())

etf_tickers=['SPY']
pl=read_eod(etf_tickers, 'US')
print(pl.tail())