# -*- coding: utf-8 -*-
"""
Author: easy00000000
Version: 0.01
Date: 2017-12-21
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pylab

from matplotlib.finance import candlestick_ohlc as ohlc_chart

# Format Data
def _match_col(col, columns):
    for c in columns:
        if col == c.lower():
            return c
        
def format_ohlc(df):
    # format to Pandas Dataframe with DateIndex
    cols = ['open', 'high', 'low', 'close']
    matched = []
    for col in cols:
        match = _match_col(col, df.columns)
        if match:
            matched.append(match)
            continue
        raise Exception('{col} not found'.format(col=col))
    formated_df = df[matched]
    formated_df.columns = cols
    formated_df.index = df.index
    formated_df.columns = ['Open', 'High', 'Low', 'Close']    
    return formated_df

# Plot Candlestick
def k_chart(self, title='', xlabel='Date', ylabel='Price', figsize_width=-1, figsize_height=-1):
    self = format_ohlc(self)
    # Structure data
    xax = np.arange(len(self.index))
    try:
        from itertools import izip
    except ImportError:
        izip = zip    
    np_ohlc = izip(xax, self['Open'], self['High'], self['Low'], self['Close'])
    # Initial
    if(figsize_width<0 or figsize_height<0):
        f_size = pylab.gcf().get_size_inches()
        figsize_width = f_size[0]*3.0
        figsize_height = f_size[1]*1.5
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_height))
    # Set Xaxis     
    date_tickers = self.index.strftime('%Y-%m-%d')
    def format_date(x, pos=None):
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]    
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
    ax.xaxis.set_major_locator(mticker.MultipleLocator(len(self.index)/figsize_width*2))
    xmin = xax[0]-1
    xmax = xax[-1]+1
    ax.set_xlim(xmin, xmax)
    # Set Xaxis Label Direction
    plt.setp(ax.get_xticklabels(), rotation=0)
    # Set Label and Title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    # Plot Data
    ohlc_chart(ax, np_ohlc, colorup='r', colordown='g') 
    # Plot Indicator
    ax.plot(xax, self.Close[1]+0*xax)
    ax.grid(True)
    # Plot ing ...
    plt.show()
    
pd.DataFrame.k_chart = k_chart
    