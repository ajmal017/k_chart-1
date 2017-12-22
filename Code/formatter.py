# -*- coding: utf-8 -*-
"""
Author: easy00000000
Version: 0.02
Date: 2017-12-22
"""
import numpy as np
import matplotlib.ticker as mticker

try:
    from itertools import izip
except ImportError:
    izip = zip

def _match_col(col, columns):
    for c in columns:
        if col == c.lower():
            return c
        
def format_ohlc(df, formated_cols=['open', 'high', 'low', 'close']):
    cols = formated_cols
    # format Dataframe as formated columns name
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
    # convert zip format
    f = formated_df
    xax = np.arange(len(df.index))
    np_ohlc = izip(xax, f[cols[0]], f[cols[1]], f[cols[2]], f[cols[3]])
    return np_ohlc

def set_ax_format(ax, tickers, fig):  
    ax = set_ax_limit(ax, tickers)    
    def format_date(x, pos=None):
        if x<0 or x>len(tickers)-1:
            return ''
        return tickers[int(x)]    
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))    
    ax = set_ax_locator(ax, tickers, fig)
    return ax

def set_ax_locator(ax, tickers, fig):
    fig_width = fig.get_size_inches()[0]
    num_tickers = len(tickers)
    unit_width = 0.5
    unit_width = 0.5 #inches
    space_width = unit_width*0.5 #space is between 2 showed tickers
    freq = num_tickers*(unit_width+space_width)//fig_width - 1
    ax.xaxis.set_major_locator(mticker.MultipleLocator(freq))
    return ax
    
def set_ax_limit(ax, tickers):
    xax = np.arange(len(tickers))
    xmin = xax[0]-1
    xmax = xax[-1]+1
    ax.set_xlim(xmin, xmax)
    return ax

def set_datetime_format(dt):
    freq_minutes = np.diff(dt).min().astype(float)/1000000000/60/60
    if freq_minutes < 24:
        datetime_format = '%Y\n%m-%d\n%H-%M'
    elif freq_minutes < 672:
        datetime_format = '%Y\n%m-%d'
    else:
        datetime_format = '%Y-%m'
    return datetime_format

def set_ticker(dt):
    datetime_format = set_datetime_format(dt)
    tickers = dt.strftime(datetime_format)
    return tickers

