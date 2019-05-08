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

from Data.get_data import read_csv
from Performance.performance import get_performance, display_performance, plot_performance
from Strategy.strategy_m1 import get_shares

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
pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss = get_performance(supporting_data, evaluated_data, get_shares)
display_performance(pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss, annual=0)
plot_performance(w, accumulated_return)
#pfm.to_csv('checking1.csv')
#s.to_csv('checking2.csv')
#w.to_csv('checking3.csv')
#accumulated_return.to_csv('checking4.csv')
'''
sy = 2004
ey = 2018
for i in range(sy,ey+1):
    end_year = i
    start_year = i
    hist_p = wp[wp.index.year<=end_year]
    hist_p = hist_p[hist_p.index.year>=start_year]
    evaluated_data = hist_p.copy()
    hist_p = wp[wp.index.year<start_year]
    supporting_data = hist_p.copy()

    # Performance for Strategy
    pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss = get_performance(supporting_data, evaluated_data, get_shares)
    display_performance(pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss)
    #plot_performance(w, accumulated_return)
'''