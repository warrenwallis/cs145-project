#!/usr/bin/env python


import sys
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
    data['close_yesterday'] = data['Close'].shift(1, fill_value=0)
    data['volume_yesterday'] = data['Volume'].shift(1, fill_value = 0)
    data['target_value'] = data.apply(lambda row: row.Close - row.Open, axis=1)
    data['target_classifier'] = data.apply(lambda row: 1 if(row.target_value > margin) else 0, axis = 1)
    data = data.shift(-1)
    data.drop(data.tail(1).index,inplace=True)
    y = data['target_classifier']
    x = data.drop(['target_classifier','Close','Volume','target_value'],axis=1)

    train_raw, test_raw, target, target_test = train_test_split(x,y, test_size=0.25, random_state=0)

    pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])

    #Transform raw data 
    train = pipeline.fit_transform(train_raw)
    test = pipeline.transform(test_raw)

    lr = LogisticRegression()
    lr.fit(train,target)
    predicted = lr.predict(test)
    print("%-12s %f" % ('Accuracy:', sklearn.metrics.accuracy_score(target_test,predicted)), file=sys.stdout)

if __name__ == '__main__':
    main()