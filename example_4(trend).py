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
from Algorithm.indicators import swt, ts_swt, cross2, ts_mean_std
from Algorithm.mkstatus import real_trend, est_trend_1
from Algorithm.mkstatus import get_match_trend, display_match_trend
from Algorithm.scale import linear_scale

# Load data
data_path = package_path + '/Data/'
source_data = pd.read_csv(data_path+'SPY2018-12-31.csv', parse_dates=True, index_col=0)

# 准备测试数据
end_year = 2018
start_year = 2014
hist_p = source_data[source_data.index.year<=end_year]
hist_p = hist_p[hist_p.index.year>=start_year]
df = hist_p.copy() #[3:n]

# calc main_indicator
#df['bolu'], df['bold'] = ts_boll(df['Adj Close'], dw=125, n_std=1.5)
# Calc Bench (Wavelet) and Post_Bi
bi_level = 6
cA, cD = swt(df['Adj Close'],bi_level+1)
if 'High' in df.columns.values:
    df['bi_post'] = bi(df['High'],df['Low'],bench=cA[bi_level])
else:
    df['bi_post'] = bi(df['Adj Close'],df['Adj Close'],bench=cA[bi_level])
cA, cD = ts_swt(df['Adj Close'],bi_level+1)
df['wt_long'] = cA[bi_level]
df['wt_short'] = cA[bi_level-2]
# calc sub_indicator
df['real_trend'] = real_trend(df['bi_post'])
df['est_trend'], df['slope'] = est_trend_1(df['wt_long'], v=0.5)
print(display_match_trend(get_match_trend(df['real_trend'], df['est_trend'])))
#df['diff_norm'] = linear_scale(df['diff'], -1, 1, min(df['diff']), max(df['diff']))
df['zeros'] = 0
# mean-std
df['mean'], df['std'] = ts_mean_std(df['Adj Close'])
df['diff'] = df['std']*df['std'] + df['mean']
df['cross'] = cross2(df['diff'], df['est_trend'], v=0.6)
# select data to plot
df = df[df.index.year>=start_year+1]

# plot ohlc candlestick
plot_chart(df,
           sub_indicator_cols=['real_trend', 'est_trend', 'cross', 'zeros'],
           bi_cols=['bi_post']
           )
