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

#from Data.get_data import fetch_eod
from get_data import save_eod

etf_tickers=['SHY','SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
#pl=fetch_eod(etf_tickers)
save_eod(etf_tickers)

hk_etf = [
        '2800', #HSI ETF
        '7300', #-1x HSI
        '0388', #港交所
        '1299', #友邦
        '2388', #中银香港
        '0002', #中电控股
        '0003', #中华燃气
        '0823', #领展
        '0066', #港铁
        '1177', #中国生物制药
        '0700', #腾讯
        '0941', #中国移动
        '0019', #太古
        '0027', #银河
        '0288', #万州
        '1044', #恒安
        '1088', #神华
        '1093' #石药
        ]
save_eod(hk_etf, 'HK')