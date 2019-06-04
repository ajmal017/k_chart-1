# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:43:12 2019

@author: w
"""
import numpy as np
import pandas as pd
import datetime
from Reporting.placement import get_value
from Data.get_data import read_price

def get_portfolio(tickers, delta_s, tickers_pl, init_cash, trans_dates, trans_prices, shares, residual_cashs, all_date=False):
    # t=0
    cash = init_cash
    portfolio = pd.DataFrame(columns=delta_s.columns)
    portfolio.loc[len(portfolio)] = np.zeros(len(tickers))
    portfolio['Date'] = delta_s.index[0]
    portfolio['Cash'] = cash
    portfolio['Value'] = 0.0    
    t = 0
    s = np.zeros(len(tickers))
    if all_date:
        start_date = delta_s.index[0]
        end_date = tickers_pl[tickers[0]].index[-1]
        range_date = pd.date_range(start=start_date, end=end_date, freq='D')
    else:
        range_date = trans_dates
    for d in range_date:
        if datetime.datetime.weekday(d)<=4:
            # calc value
            portfolio.loc[len(portfolio)] = portfolio.loc[len(portfolio)-1]
            if d == trans_dates[t]:
                s = shares[t]
                for e in range(len(tickers)):                
                    portfolio[tickers[e]].iloc[-1] = s[e]  
                cash = residual_cashs[t]
                if t < len(trans_dates)-1:
                    t = t + 1
            portfolio['Date'].iloc[-1] = d
            portfolio['Cash'].iloc[-1] = cash
            portfolio['Value'].iloc[-1] = get_value(tickers, d, s, tickers_pl)
    portfolio.set_index("Date", inplace=True)
    return portfolio

def mapping(tickers, delta_s, tickers_pl, init_cash, trans_dates, trans_prices, shares, residual_cashs, freq='D'): 
    #freq: T-trading date, D-Daily, W-Weekly, M-Monthly
    # t=0
    mapping_date = []
    d = delta_s.index[0]
    mapping_date.append(d)
    mapping_cash = []
    cash = init_cash
    mapping_cash.append(cash)    
    mapping_shares = []
    s = np.zeros(len(tickers))
    mapping_shares.append(s)
    mapping_closes = []
    c = np.zeros(len(tickers))   
    pre_t_date = delta_s.index[0] + datetime.timedelta(days=-1)    
    for e in range(len(tickers)):
        while pre_t_date.date() not in tickers_pl[tickers[e]].index.date:
            pre_t_date = pre_t_date + datetime.timedelta(days=-1)
        p = read_price(pre_t_date, tickers[e], tickers_pl[tickers[e]])
        c[e] = p.Close    
    mapping_closes.append(c)
    mapping_value = []
    v = 0.0
    mapping_value.append(v)
    # t>=1
    if freq == 'D':
        start_date = delta_s.index[0]
        end_date = tickers_pl[tickers[0]].index[-1]
        range_date = pd.date_range(start=start_date, end=end_date, freq='D')
    elif freq == 'T':
        range_date = trans_dates
    else:
        range_date = trans_dates
    t = 0
    for d in range_date:
        if datetime.datetime.weekday(d)<=4:
            if d == trans_dates[t]:
                s = shares[t]
                cash = residual_cashs[t]
                if t < len(trans_dates)-1:
                    t = t + 1
            mapping_date.append(d)
            mapping_cash.append(cash)
            mapping_shares.append(s)
            c = mapping_closes[-1]
            for e in range(len(tickers)):
                if d.date() in tickers_pl[tickers[e]].index.date:
                    p = read_price(d, tickers[e], tickers_pl[tickers[e]])
                c[e] = p.Close
            mapping_closes.append(c)
            v = sum(s*c)
            mapping_value.append(v)
    return mapping_date, mapping_shares, mapping_closes, mapping_cash, mapping_value
                
    