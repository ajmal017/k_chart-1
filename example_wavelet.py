# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 10:10:17 2018
@author: easy000000000
"""

import numpy as np
import pandas as pd
from KChart import k_chart
from Algorithm.swt import ts_swt

# Read Data
source_data = pd.read_csv('spy.csv', parse_dates=True, index_col=0)
df = source_data.copy()
# Calc Wavelet
cA, cD = ts_swt(df['Close'],6)
# Assign values
df['wt']=cA[4]
# plot
df.k_chart(main_indicator_cols='wt')