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
from BackTesting.backtesting import plot_performance, get_figname, csv_performance
from Strategy.strategy_m4_plus import get_shares

# 读取数据
etf_tickers=['SHY','SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
basic_tickers = ['SHY','SPY','XLB','XLE','XLF','XLI','XLK','XLP','XLU','XLV','XLY']
#basic_tickers = ['SHY','SPY']
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
start_year = 2018
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
result = display_performance(w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss, annual=0)
figname = get_figname(start_year, end_year)
show_indicators = indicators[indicators.columns[:2]]
plot_performance(w, accumulated_return, show_indicators, figname)
csv_file = get_figname(start_year, end_year, 'csv')
csv_performance(csv_file, 'w', w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss, annual=0)
share_file = get_figname('', end_year, 'csv')
s.to_csv(share_file, encoding='utf-8')
# Performance for each year
for n in range(start_year, end_year+1):
    w_n = w[w.index.year==n]
    ar_n = accumulated_return[accumulated_return.index.year==n]
    ind_n = indicators[indicators.index.year==n]
    w_n, ar_n, total_return, annual_return, annual_std, sharpe_ratio, max_loss = get_performance_by_results(w_n, ar_n)
    result = display_performance(w_n, ar_n, total_return, annual_return, annual_std, sharpe_ratio, max_loss)
    figname = get_figname(n, n)
    #plot_performance(w_n, ar_n, ind_n[ind_n.columns[:2]], figname)
    csv_performance(csv_file, 'a', w_n, ar_n, total_return, annual_return, annual_std, sharpe_ratio, max_loss)