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
import numpy as np
from time import process_time

from Data.get_data import read_csv
from Strategy.rotation import select_assets
from BackTesting.backtesting import get_performance, display_performance, get_performance_total
from BackTesting.backtesting import plot_performance, get_figname
from Strategy.strategy_m2 import get_shares

# set end_date
end_date = '2018-12-31'
# 读取数据
etf_tickers=['SHY','SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
pl=read_csv(etf_tickers, end_date)
potential_tickers=['SPY','XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY']
# 选择时间
end_year = 2018
start_year = 2014
# back testing
basic_tickers = ['SHY', 'SPY']
mc_budget = [0.0, 0.6, 0.2, 0.2]
#basic_tickers = ['SPY']
#mc_budget = [0.6, 0.2, 0.2]
sw_tickers = basic_tickers.copy()
sar_tickers = basic_tickers.copy()+['Portfolio']
sw = pd.DataFrame(columns=sw_tickers)
sar = pd.DataFrame(columns=sar_tickers)
sar_times = pd.Series(np.zeros(len(sar_tickers)), index=sar_tickers)
for i in range(start_year, end_year+1):
    selected_tikcers = basic_tickers.copy()
    previous_year = i-1
    evaluated_year = i    
    # 准备测试数据
    pli = pl[pl.index.year<=evaluated_year]
    # 周线
    wp = pli.resample('W', loffset=pd.offsets.timedelta(days=-6)).mean()
    # 选择资产类别
    hist_p = wp[wp.index.year==previous_year]
    hist_p = hist_p[potential_tickers]
    selected_assets = select_assets(hist_p)
    for e in enumerate(selected_assets):
        selected_tikcers.append(e[1])
    # 准备测试数据
    wp = wp[selected_tikcers]
    evaluated_data = wp[wp.index.year==evaluated_year]
    supporting_data = wp[wp.index.year<=previous_year]
    # Performance for Strategy
    start_time = process_time()
    pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss, risk_bias = get_performance(supporting_data, evaluated_data, get_shares, mc_budget)
    print('Running Time: ', process_time()-start_time)
    print('Total Risk Bias: ', risk_bias)
    display_performance(w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss)
    figname = get_figname(evaluated_year, evaluated_year)
    plot_performance(w, accumulated_return, figname)
    # accumulate
    sw = pd.concat([sw, w[sw_tickers]], axis=0)
    sar_tmp = accumulated_return[sar_tickers].copy() + sar_times
    sar = pd.concat([sar,sar_tmp], axis=0)
    sar_times = sar.iloc[-1][sar_tickers]
# Total
w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss = get_performance_total(sw, sar)
display_performance(w, accumulated_return, total_return, annual_return, annual_std, sharpe_ratio, max_loss, annual=0)
figname = get_figname(start_year, end_year)
plot_performance(sw, sar, figname)
    