# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:27:51 2019

@author: w
"""
import numpy as np
from KChart import figure
import matplotlib.pyplot as plt
from time import time

def get_performance(supporting_data, evaluated_data, strategy_function, *args, **kwargs):
    # strategy_function gets shares position for t
    # historical data of each asset in portfolio
    
    # initial
    initial_cash = 1000000
    last_shares = np.zeros(len(evaluated_data.columns))
    last_cash = initial_cash
    
    zl = np.zeros(len(evaluated_data))
    pfm = evaluated_data.copy()    
    pfm = pfm.assign(Portfolio=zl)   
    s = evaluated_data.copy()
    s = s.assign(Cash=zl)
    w = evaluated_data.copy()
    
    histp_series = supporting_data.copy()
    
    for t in range(0, len(evaluated_data)):
        shares, cash = strategy_function(histp_series, last_shares, last_cash, *args, **kwargs)
        pfm['Portfolio'][t] = 0.0
        for e in range(0, len(shares)):
            s[s.columns[e]][t]=shares[e]
            pfm['Portfolio'][t] = pfm['Portfolio'][t] + shares[e]*pfm[pfm.columns[e]][t]
        s['Cash'][t] = cash
        pfm['Portfolio'][t] = pfm['Portfolio'][t] + cash
        w.iloc[t] = _real_weights(evaluated_data.iloc[t], pfm['Portfolio'][t], shares)
        # for next step
        last_shares = shares
        last_cash = cash
        histp_series = histp_series.append(evaluated_data.iloc[t])    
    
    accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss = _get_results(pfm, supporting_data, initial_cash)
    
    return pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss

def _real_weights(p, v, s):
    w = np.zeros(len(s))
    for e in range(0,len(s)):
        w[e] = s[e]*p[e] / v
    return w

def _get_results(original_pfm, supporting_data, initial_cash, annual_factor=52):
    # structure 0-1 data
    zl = np.zeros(len(supporting_data))
    spd = supporting_data.copy()    
    spd = spd.assign(Portfolio=zl)
    spd['Portfolio'][-1] = initial_cash
    pfm = original_pfm.copy()
    pfm = pfm.append(spd.iloc[-1])
    pfm = pfm.sort_index()
       
    # accumulated return
    r = pfm.copy()
    acm_r = pfm.copy()
    for e in pfm.columns:
        r[e]=r[e].pct_change()
        r[e][0]=0.0
        acm_r[e][0]=0.0
        for t in range(1,len(r)):        
            acm_r[e][t]=(1+r[e][t])*(1+acm_r[e][t-1])-1    
    accumulated_return = acm_r
    
    # totalreturn
    total_return = []
    for e in pfm.columns:
        total_return.append(acm_r[e][len(r)-1])
        
    # annualized return and std
    annual_return = []
    annual_std = []
    r = pfm.copy()
    rsq = pfm.copy()
    for e in pfm.columns:
        r[e] = r[e].pct_change()
        annual_return.append(np.power(1+r[e].mean(), annual_factor)-1)
        rsq[e] = r[e]*r[e]
        annual_std.append(np.power(annual_factor*rsq[e].mean(),0.5))
        
    # sharp ratio
    sharp_ratio = []
    for i in range(0, len(pfm.columns)):
        sharp_ratio.append(annual_return[i]/annual_std[i])
        
    # max loss
    max_loss = []
    p = pfm.copy()
    for e in pfm.columns:
        m=0
        for t in range(1,len(p)):
            d = min(p[e][t:len(p)])/p[e][t-1] - 1
            if m>d:
                m=d
        max_loss.append(m)
    
    return accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss

def display_performance(pfm, s, w, accumulated_return, total_return, annual_return, annual_std, sharp_ratio, max_loss, annual=1):
    start_time = str(pfm.index[0])
    end_time = str(pfm.index[-1])
    ep = '{:20}'.format('Evaluated Period:') + start_time[0:10] + ' to ' + end_time[0:10]
    
    title = '{:20}'.format('Assets:')
    for e in pfm.columns:
        title= title + '{:>12}'.format(e)
        
    tr ='{:20}'.format('Total Return')
    ar ='{:20}'.format('Annualized Return')
    std = '{:20}'.format('Annualized STD')
    spr = '{:20}'.format('Sharp Ratio')
    mloss = '{:20}'.format('Max Loss')
    for i in range(0, len(total_return)):
        tr = tr + '{:>12}'.format('%0.2f%%' %(total_return[i]*100))
        ar = ar + '{:>12}'.format('%0.2f%%' %(annual_return[i]*100))
        std = std + '{:>12}'.format('%0.2f%%' %(annual_std[i]*100))
        spr = spr + '{:>12}'.format('%0.2f' %(sharp_ratio[i]))
        mloss = mloss + '{:>12}'.format('%0.2f%%' %(max_loss[i]*100))
    
    # annual = 1 : for each year
    if annual > 0:
        prn_txt =   ep + '\n' + \
                    title + '\n' + \
                    ar + '\n' + \
                    std + '\n' + \
                    spr + '\n' + \
                    mloss
    else:
        prn_txt =   ep + '\n' + \
                    title + '\n' + \
                    tr + '\n' + \
                    ar + '\n' + \
                    std + '\n' + \
                    spr + '\n' + \
                    mloss
    print(prn_txt)
    return prn_txt

def plot_performance(weights, accumulated_return, figname=None):
    ar = accumulated_return.copy()
    # Set rows of figure
    rows = 2
    cols = 1
    
    # Set figure and gridspec
    fig = figure.set_fig(-1, -1, rows=rows)
    gs = figure.set_gs(rows, cols=cols, height_ratios=2)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.set_xlim(ar.index[0], ar.index[-1])
    ax2.set_xlim(ar.index[0], ar.index[-1])
    
    for i in range(0,len(ar.columns)-1):
        ax1.plot(ar[ar.columns[i]], linewidth=2)
    ax1.plot(ar[ar.columns[len(ar.columns)-1]], color='black', linewidth=4)
    ax1.legend()
    
    ax2.stackplot(weights.index, weights.values.T)
    
    if figname != None:    
        fig.savefig(figname) # save the figure to file
        plt.close(fig)
        
def get_figname(start_year, end_year):
    figname = str(time()).split('.')[0]
    if start_year == end_year:
        figname = figname + '(' + str(start_year) + ').jpg'
    else:
        figname = figname + '(' + str(start_year) + '-' + str(end_year) + ').jpg'
    return figname