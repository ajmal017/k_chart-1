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
from BackTesting.backtesting import get_performance, display_performance
from BackTesting.backtesting import plot_performance, get_figname
from Strategy.strategy_m2 import get_shares

# set end_date
end_date = '2018-12-31'
# 读取数据
etf_tickers=['SHY','SPY','XLE','XLF']
pl=read_csv(etf_tickers, end_date)
portfolio = 'Portfolio'
#周线
wp = pl.resample('W', loffset=pd.offsets.timedelta(days=-6)).mean().dropna()

# 准备测试数据
end_year = 2018
start_year = 2013
hist_p = wp[wp.index.year<=end_year]
hist_p = hist_p[hist_p.index.year>=start_year]
evaluated_data = hist_p.copy()
hist_p = wp[wp.index.year<start_year]
supporting_data = hist_p.copy()

# Performance for Strategy
start_time = process_time()
pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss, risk_bias = get_performance(supporting_data, evaluated_data, get_shares)
print('Running Time: ', process_time()-start_time, 's')
print('Total Risk Bias: ', risk_bias)
title = display_performance(pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss, annual=0)
figname = get_figname(start_year, end_year)
plot_performance(w, accumulated_return, figname)
#pfm.to_csv('checking1.csv')
#s.to_csv('checking2.csv')
#w.to_csv('checking3.csv')
#accumulated_return.to_csv('checking4.csv')
'''
sy = start_year
ey = end_year
for i in range(sy,ey+1):
    end_year = i
    start_year = i
    hist_p = wp[wp.index.year<=end_year]
    hist_p = hist_p[hist_p.index.year>=start_year]
    evaluated_data = hist_p.copy()
    hist_p = wp[wp.index.year<start_year]
    supporting_data = hist_p.copy()

    # Performance for Strategy
    start_time = process_time()
    pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss, risk_bias = get_performance(supporting_data, evaluated_data, get_shares)
    print('Running Time: ', process_time()-start_time)
    print('Total Risk Bias: ', risk_bias)
    display_performance(pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss)
    figname = get_figname(start_year, end_year)
    plot_performance(w, accumulated_return, figname)
'''