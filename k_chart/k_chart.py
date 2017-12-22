# -*- coding: utf-8 -*-
"""
Author: easy00000000
Version: 0.12
Date: 2017-12-22
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from k_chart import figure
from k_chart import formatter as fmt
from k_chart import plotter

# Plot Candlestick
def k_chart(self, 
            figsize_width=-1, figsize_height=-1, 
            main_indicator_cols=None, 
            volume_col=None, 
            sub_indicator_cols=None):
    
    # Set rows of figure
    rows = figure.get_rows(volume_col, sub_indicator_cols)
    cols = 1
    
    # Set figure and gridspec
    fig = figure.set_fig(figsize_width, figsize_height, rows=rows)
    gs = figure.set_gs(rows, cols=cols)
    
    # Set ax_%%%
    ax_main = fig.add_subplot(gs[0, 0])
    plt.setp(ax_main.get_xticklabels(), rotation=0)
    ax_vol = None
    ax_sub = None
    if volume_col != None:
        ax_vol = fig.add_subplot(gs[1, 0], sharex=ax_main)
        plt.setp(ax_main.get_xticklabels(), visible=False)
        if sub_indicator_cols != None:
            ax_sub = fig.add_subplot(gs[2, 0], sharex=ax_main)
            plt.setp(ax_vol.get_xticklabels(), visible=False)
    else:
        if sub_indicator_cols != None:
            ax_sub = fig.add_subplot(gs[1, 0], sharex=ax_main)
            plt.setp(ax_main.get_xticklabels(), visible=False)

    # Plot Main Figure        
    # Set Axis     
    date_tickers = fmt.set_ticker(self.index) #strftime('%Y\n%m-%d')
    ax_main = fmt.set_ax_format(ax_main, fig, tickers=date_tickers, ylabel='Price') 
       
    # Structure ohlc data
    ohlc_cols=['open', 'high', 'low', 'close']
    np_ohlc = fmt.format_ohlc(self, formated_cols=ohlc_cols)
    # ---
    plotter.plot_ohlc(ax_main, np_ohlc)
    # ---
    if main_indicator_cols != None:        
        plotter.plot_y(ax_main, self[main_indicator_cols].values)
    
    # Plot Volume Figure
    if ax_vol != None:
        # Set Axis
        ax_vol = fmt.set_ax_format(ax_vol, fig, ylabel=volume_col)
        # ---
        plotter.plot_bar(ax_vol, self[volume_col].values)
        
    # Plot Sub_Indicator Figure
    if ax_sub != None:
        # Set Axis
        ax_sub = fmt.set_ax_format(ax_sub, fig, ylabel=sub_indicator_cols)
        # ---
        plotter.plot_y(ax_sub, self[sub_indicator_cols].values)
    
pd.DataFrame.k_chart = k_chart
    