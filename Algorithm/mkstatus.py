# -*- coding: utf-8 -*-
"""
Author: easy00000000
Version: 0.10
Date: 2018-01-05
"""

import numpy as np

def trend(bi, v=1.0):
    t = np.zeros(len(bi))
    p = 0
    for i in range(1,len(bi)):
        if bi[i-1] > 0:
            p = -v
        elif bi[i-1] < 0:
            p = v
        t[i] = p
    return t

def strong(bi, tr=None, t=0.02, v=0.5):
    s = np.zeros(len(bi))
    pos1 = 0
    for i in range(1,len(bi)):        
        if bi[i]>0:            
            if -bi[i]/bi[pos1]-1>t:
                for j in range(pos1+1,i+1):
                    s[j] = v
            pos1 = i
        elif bi[i]<0:
            if -bi[pos1]/bi[i]-1>t:
                for j in range(pos1+1,i+1):
                    s[j] = -v
            pos1 = i
    if tr is not None:
        for i in range(len(bi)):
            if tr[i]>0 and s[i]<0:
                s[i] = 0.
            elif tr[i]<0 and s[i]>0:
                s[i] = 0.                
    return s