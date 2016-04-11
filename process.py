import requests
import pandas as pd 
import re
import os
from plot import produce_plot
from bokeh.embed import components

QUANDL_API = os.environ["QUANDL_API"]

def process_input(tickers):
    patt = re.compile(r"\W+")
    querys = re.split(patt, tickers.strip())
    querys = [val.upper() for val in querys]
    return querys

url = "https://www.quandl.com/api/v3/datasets/WIKI/"
ftype = ".csv"
APIKEY = {'api_key':QUANDL_API}

def request_to_df(r, options):
    options.insert(0,'Date')
    df = pd.read_csv(r.url, index_col='Date', usecols = options)[::-1]
    df.index = pd.to_datetime(df.index)
    return df

def get_data(query, options):
    df = {}
    query = process_input(query)
    for item in query:
        r = requests.get(url+item+ftype,APIKEY)
        if r.ok:
            df[item] = request_to_df(r, options)
        else:
            df[item] = None
    return df
def make_html(query, options):
    data = get_data(query, options)
    notValid = []
    for key in dict(data):
        if data[key] is None:
            notValid.append(key)
            del data[key]
    plotTickers = produce_plot(data)
    #save(plotTickers)
    return (notValid,plotTickers)
