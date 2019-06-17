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
from Algorithm.mkstatus import real_trend, est_trend_1
from Algorithm.scale import linear_scale

# Load data
data_path = package_path + '/Data/'
source_data = pd.read_csv(data_path+'2833.csv', parse_dates=True, index_col=0)

# 准备测试数据
end_year = 2018
start_year = 2013
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
#df['diff'] = df['wt_short'] - df['wt_long']
#df['diff_norm'] = linear_scale(df['diff'], -1, 1, min(df['diff']), max(df['diff']))
df['dn_line'] = -0.01
df['up_line'] = 0.02
#
df['est_trend'], df['slope'] = est_trend_1(df['wt_long'])
df['ma'] = df['Adj Close'].rolling(64,center=True,min_periods=1).mean()
df['est_trend_ma'], df['slope_ma'] = est_trend_1(df['ma'])

# select data to plot
df = df[df.index.year>=start_year+1]
# plot ohlc candlestick
plot_chart(df,
           sub_indicator_cols=['slope', 'dn_line', 'up_line'],
           bi_cols=['bi_post']
           )
