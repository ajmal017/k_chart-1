# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 17:36:21 2018
@author: easy000000000
"""

import numpy as np
import pandas as pd

from KChart import k_chart
from Algorithm.twinety import bi
from Algorithm.swt import swt, ts_swt

# Load data
source_data = pd.read_csv('spy.csv', parse_dates=True, index_col=0)

# Calc
n=256
df=source_data #[3:n]
# calc sub_indicator
df['diff'] = df['Adj Close']/df['Close']
# bi
df['bi'] = bi(df['High'],df['Low'])
# Calc Bench (Wavelet)
cA, cD = swt(df['Close'],6)
df['wt']=cA[1]
df['bi1'] = bi(df['High'],df['Low'],bench=cA[1])
df['bi2'] = bi(df['High'],df['Low'],bench=cA[2])
# calc main_indicator
cA, cD = ts_swt(df['Close'],6)
df['wt']=cA[2]
# calc main_indicator
df['ma'] = df['Close'].rolling(12,center=True,min_periods=1).mean()

# plot ohlc candlestick
df.k_chart(
        main_indicator_cols=['wt','ma'],
        volume_col=['Volume'], 
        sub_indicator_cols=['diff'], 
        bi_cols=['bi2','bi1','bi']
        )