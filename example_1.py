# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 23:07:08 2017
@author: easy000000000
"""

import numpy as np
import pandas as pd

from k_chart import k_chart

# Load data
source_data = pd.read_csv('spy.csv', parse_dates=True, index_col=0)

# Calc
df=source_data.copy()
# calc sub_indicator
df['diff'] = df['Adj Close']/df['Close']
# calc main_indicator
df['ma'] = df['Close'].rolling(12,center=True,min_periods=1).mean()

# plot ohlc candlestick
df.k_chart(main_indicator_cols='ma', volume_col='Volume', sub_indicator_cols='diff')