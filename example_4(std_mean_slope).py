# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:03:48 2019

@author: w
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
from Algorithm.indicators import ts_mean_std, ts_swt, swt, cross
from Algorithm.mkstatus import real_trend, est_trend_1
from Algorithm.mkstatus import display_match_trend, get_match_trend
from Algorithm.scale import linear_scale

# Load data
data_path = package_path + '/Data/'
source_data = pd.read_csv(data_path+'XLE2018-12-31.csv', parse_dates=True, index_col=0)

# 准备测试数据
end_year = 2018
start_year = 2003
hist_p = source_data[source_data.index.year<=end_year]
hist_p = hist_p[hist_p.index.year>=start_year]
df = hist_p.copy()

# Calc Bench (Wavelet) and Post_Bi
bi_level = 4
cA, cD = swt(df['Adj Close'],bi_level+1)
if 'High' in df.columns.values:
    df['bi_post'] = bi(df['High'],df['Low'],bench=cA[bi_level])
else:
    df['bi_post'] = bi(df['Adj Close'],df['Adj Close'],bench=cA[bi_level])
cA, cD = ts_swt(df['Adj Close'],bi_level+1)
# calc sub_indicator
df['real_trend'] = real_trend(df['bi_post'])
df['mean'], df['std'] = ts_mean_std(df['Adj Close'])
df['diff'] = df['std']*df['std'] + df['mean']
#df['cross'] = cross(df['diff'], v=0.01)
df['zeros'] = 0
#
df['est_trend'], df['slope'] = est_trend_1(df['diff'])

# select data to plot
df = df[df.index.year>=start_year+1]
# plot ohlc candlestick
plot_chart(df,
           sub_indicator_cols=['slope', 'zeros'],# 'cross'],
           bi_cols=['bi_post']
           )