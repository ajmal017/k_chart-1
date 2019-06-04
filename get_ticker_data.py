# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:54:00 2019

@author: w
"""

import requests
import pandas as pd
from pandas.compat import StringIO

# https://eodhistoricaldata.com/api/eod/AAPL.US?api_token={your_api_key}
def get_historical_data(symbol="AAPL.US", api_token="5cebe613e02010.08022109", session=None):
    if session is None:
        session = requests.Session()        
        url = "https://eodhistoricaldata.com/api/eod/%s" % symbol        
        params = {        
            "api_token": api_token        
        }
        r = session.get(url, params=params)
        if r.status_code == requests.codes.ok:
            df = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine="python")
        return df
    else:
        raise Exception(r.status_code, r.reason, url)
        
ticker = 'SHY'
print(get_historical_data(ticker).tail())