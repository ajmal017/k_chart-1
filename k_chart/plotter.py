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
    
def plot_y(ax, y):
    xax = np.arange(len(y))
    ax.plot(xax, y)
    
def plot_bar(ax, h): #h: height of bar
    xax = np.arange(len(h))
    ax.bar(xax, h)