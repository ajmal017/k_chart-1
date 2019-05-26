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
from BackTesting.backtesting import display_performance, get_performance_by_results
from BackTesting.backtesting import plot_performance, get_figname
from Strategy.strategy_m2_plus_multi import get_shares

# set end_date
end_date = '2018-12-31'
# 读取数据
etf_tickers=['SHY','SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
basic_tickers = ['SHY','SPY','XLB','XLE','XLF','XLI','XLK','XLP','XLU','XLV','XLY']
etf_tickers = basic_tickers 
mc_budget = [0.78, 0.22, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00] #
pl=read_csv(etf_tickers, end_date)
#周线
wp = pl.resample('W', loffset=pd.offsets.timedelta(days=-6)).mean().dropna()
# 选择时间
end_year = 2018
start_year = 2004
hist_p = wp[wp.index.year<=end_year]
hist_p = hist_p[hist_p.index.year>=start_year]
evaluated_data = hist_p.copy()
hist_p = wp[wp.index.year<start_year]
supporting_data = hist_p.copy()
# back testing
# Performance for Strategy
start_time = process_time()
pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss, indicators = get_performance(supporting_data, evaluated_data, mc_budget, get_shares)
print('Running Time: ', process_time()-start_time)
display_performance(w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss, annual=0)
figname = get_figname(start_year, end_year)
plot_performance(w, accumulated_return, indicators, figname)
# Performance for each year
for n in range(start_year, end_year+1):
    w_n = w[w.index.year==n]
    ar_n = accumulated_return[accumulated_return.index.year==n]
    ind_n = indicators[indicators.index.year==n]
    w_n, ar_n, total_return, annual_return, annual_std, sharpe_ratio, max_loss = get_performance_by_results(w_n, ar_n)
    display_performance(w_n, ar_n, total_return, annual_return, annual_std, sharpe_ratio, max_loss)
    figname = get_figname(n, n)
    plot_performance(w_n, ar_n, ind_n, figname)