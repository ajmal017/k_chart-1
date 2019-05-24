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

from KChart import k_chart
from Algorithm.twinety import bi
from Algorithm.swt import swt, ts_swt
from Algorithm.mkstatus import trend

# Load data
data_path = package_path + '/Data/'
source_data = pd.read_csv(data_path+'spy2018-12-31.csv', parse_dates=True, index_col=0)

# Calc
df=source_data #[3:n]

# Calc Bench (Wavelet) and Post_Bi
bi_level = 6
cA, cD = swt(df['Adj Close'],bi_level+1)
df['wt']=cA[bi_level]
df['bi_post'] = bi(df['High'],df['Low'],bench=cA[bi_level])
# calc main_indicator
#cA, cD = ts_swt(df['Close'],6)
#df['wt']=cA[6]
# calc sub_indicator
df['trend'] = trend(df['bi_post'])

# plot ohlc candlestick
df.k_chart(
        main_indicator_cols=['wt'],
        volume_col=['Volume'], 
        sub_indicator_cols=['trend'], 
        bi_cols=['bi_post']
        )
