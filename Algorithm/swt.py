# -*- coding: utf-8 -*-
"""
Author: easy00000000
Version: 0.01
Date: 2018-01-03
"""
import numpy as np

def swt(data, level):
    # level: swt level and should be >0
    ln=len(data)    
    lo=hi=lo2=hi2=0    
    cA = np.zeros((level, ln))
    cD = np.zeros((level, ln))
    for l in range(level):
        if l==0:
            t=data.copy()
        else:
            t=cA[l-1].copy()
        two=2**l
        two2=2**(l+1)
        # if data length is not enough (less than 2**level+1)
        # then not calculate and keep ZERO in these levels
        if ln>two2:
            for i in range(ln):
                lo=abs(i-two)
                hi=i+two
                if hi>=ln:
                    hi=ln+ln-hi-2           
                lo2=abs(i-two2)
                hi2=i+two2
                if hi2>=ln:
                    hi2=ln+ln-hi2-2
                cA[l][i]=(((t[lo2]+t[hi2])/16)+((t[lo]+t[hi])/4)+(3*t[i]/8))
            if l>0:
                cD[l] = cA[l-1] - cA[l]
    cD[0] = data - cA[0]
    return cA, cD

def ts_swt(data, level):
    ln=len(data)
    m=2**level
    # if data length is not enough (less than 2**level+1)
    # then just do static swt
    if ln>m+1:        
        cA = np.zeros((level, ln))
        cD = np.zeros((level, ln))
        # for data between 0:m
        cA[:,:m+1], cD[:,:m+1] = swt(data[0:m+1], level)
        # for data between m+1:ln-1
        for i in range(m+1,ln):
            tcA, tcD = swt(data[i-m:i+1], level)
            for l in range(level):
                cA[:,i], cD[:,i] = tcA[:,-1], tcD[:,-1]
    else:
        cA, cD = swt(data, level)
    return cA, cD