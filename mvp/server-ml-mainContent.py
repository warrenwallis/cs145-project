#!/usr/bin/env python


import sys, json
import yfinance as yf

import sklearn, numpy as np, scipy as scp, pandas as pd, matplotlib.pyplot as plt, matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, Binarizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, Normalizer, MinMaxScaler
from sklearn.compose import ColumnTransformer, make_column_transformer

margin = 0

def main():
    comp = yf.Ticker(sys.argv[1])
    data = comp.history(period='1y')
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    today = data[len(data) - 1:]
    today = today\
        .assign(Name = comp.info['shortName'])\
        .assign(Symbol = '(' + comp.info['symbol'] + ')')
    today_json = today.to_json(orient='records')
    print(today_json, file=sys.stdout)
    

if __name__ == '__main__':
    main()