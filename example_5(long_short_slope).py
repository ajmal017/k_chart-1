# -*- coding: utf-8 -*-
"""
Created on Wed Jan 3 17:36:21 2018
@author: easy000000000
Modified on Sun Mar 3 2019
"""
# add to syspath
import os
import sys
package_path = os.getcwd()
if package_path not in sys.path:
    sys.path.append(package_path)

import pandas as pd

from KChart.plot_chart import plot_chart
from Algorithm.twinety import bi
from Algorithm.indicators import swt, ts_swt
from Algorithm.mkstatus import est_trend_1
from Data.get_data import read_csv

# Load data
# set end_date
end_date = '2018-12-31'
# 读取数据
etf_tickers=['SPY']
source_data = read_csv(etf_tickers, end_date)

# 准备测试数据
end_year = 2018
start_year = 2003
hist_p = source_data[source_data.index.year<=end_year]
hist_p = hist_p[hist_p.index.year>=start_year]
wp = hist_p.resample('W', loffset=pd.offsets.timedelta(days=-6)).mean()
df = wp.copy() #[3:n]

# Calc Bench (Wavelet) and Post_Bi
bi_level = 4
cA, cD = swt(df[etf_tickers].get_values(), bi_level+1)
df['bi_post'] = bi(df[etf_tickers].get_values(),df[etf_tickers].get_values(),bench=cA[bi_level])
cA, cD = ts_swt(df[etf_tickers].get_values(),bi_level+1)
df['wt_long'] = cA[bi_level]
# calc sub_indicator
df['dn_line'] = -0.02
df['up_line'] = 0.08
#
df['est_trend'], df['slope'] = est_trend_1(df['wt_long'])

# select data to plot
df = df[df.index.year>=start_year+1]
df['Adj Close'] = df[etf_tickers]
# plot ohlc candlestick
plot_chart(df,
           sub_indicator_cols=['slope', 'dn_line', 'up_line'],
           bi_cols=['bi_post']
           )
