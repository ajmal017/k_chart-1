# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:53:54 2019

@author: w
"""
import os
import sys
package_path = os.getcwd()
if package_path not in sys.path:
    sys.path.append(package_path)
import pandas as pd
from time import process_time

from Data.get_data import read_csv
from BackTesting.backtesting import get_performance_2 as get_performance
#from BackTesting.backtesting import get_figname
from Reporting.display import get_filename
from Strategy.strategy_m5 import get_shares

# 读取数据
etf_tickers=[
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
basic_tickers = ['SHY','2800','0002','0003','0019','0066','0388','0941','1044','1093','2388']
etf_tickers = basic_tickers 
mc_budget = [0.8, 0.2]
if len(etf_tickers)>2:
    for e in range(2,len(etf_tickers)):
        mc_budget.append(0.0)
pl=read_csv(etf_tickers)
#周线
wp = pl.resample('W', loffset=pd.offsets.timedelta(days=0)).last().dropna()
# 选择时间
end_year = 2019
start_year = 2004
hist_p = wp[wp.index.year<=end_year]
hist_p = hist_p[hist_p.index.year>=start_year]
evaluated_data = hist_p.copy()
hist_p = wp[wp.index.year<start_year]
supporting_data = hist_p.copy()
# back testing
# Performance for Strategy
start_time = process_time()
pfm, s, w, accumulated_return, total_return, \
    annual_return, annual_std, sharpe_ratio, \
    max_loss, indicators = get_performance(\
    supporting_data, evaluated_data, mc_budget, get_shares)
print('Running Time: ', process_time()-start_time)
s_d = s.diff()
s_d.iloc[0] = s.iloc[0]
s_d = s_d.drop(['Cash'], axis=1)
s_d = s_d.drop(s_d.index[-1])
share_file = get_filename(start_year, end_year, 'xlsx', 'Reporting\\results')
s_d.to_excel(share_file, encoding='utf-8')