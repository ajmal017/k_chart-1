# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:58:02 2019

@author: w
"""

from Data.get_data import get_weekend_date
from Data.get_data import read_price

t_date = '2019-5-26'
ticker = 'SHY'
'''
w_date = get_weekend_date(t_date)
print(w_date)
w_date = get_weekend_date(t_date, True)
print(w_date)
'''
p = read_price(t_date, ticker, True)
print(p)