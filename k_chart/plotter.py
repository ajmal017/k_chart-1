# -*- coding: utf-8 -*-
"""
Author: easy00000000
Version: 0.02
Date: 2017-12-22
"""
import numpy as np
from matplotlib.finance import candlestick_ohlc

def plot_ohlc(ax, ohlc):
    candlestick_ohlc(ax, ohlc, colorup='r', colordown='g')
    
def plot_main(ax, indicator):
    xax = np.arange(len(indicator))
    ax.plot(xax, indicator)
    
def plot_vol(ax, vol):
    xax = np.arange(len(vol))
    ax.bar(xax, vol)
    
def plot_sub(ax, indicator):
    xax = np.arange(len(indicator))
    ax.plot(xax, indicator)