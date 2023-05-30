#!/usr/bin/env python


import sys, json, requests
import yfinance as yf

import sklearn, numpy as np, scipy as scp, pandas as pd, matplotlib.pyplot as plt, matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, Binarizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, Normalizer, MinMaxScaler
from sklearn.compose import ColumnTransformer, make_column_transformer

margin = 4
period_of_time = '1y'
number_of_past_days = 7
meta = 7
urls = {
    'SMA': ['https://www.alphavantage.co/query?function=SMA&symbol=', '&interval=daily&time_period=10&series_type=open&apikey=V9JMVK5EVUZZ2KPV'],
    'RSI': ['https://www.alphavantage.co/query?function=RSI&symbol=', '&interval=daily&time_period=10&series_type=open&apikey=V9JMVK5EVUZZ2KPV'],
    'MFI': ['https://www.alphavantage.co/query?function=MFI&symbol=', '&interval=daily&time_period=10&apikey=V9JMVK5EVUZZ2KPV'],
    'STOCH': ['https://www.alphavantage.co/query?function=STOCH&symbol=', '&interval=daily&apikey=V9JMVK5EVUZZ2KPV']
}

def queryAV(param, comp):
    url_arr = urls[param]
    url = url_arr[0] + comp + url_arr[1]
    r = requests.get(url)
    data = r.json()
    df = pd.json_normalize(data, max_level=2).T
    df = df[meta:]
    df = df.iloc[::-1]

    return df


def getQueries(query):
    return query.split('/')

def main():
    queries = getQueries(sys.argv[1])
    comp = yf.Ticker(queries[0])
    sym = comp.info['symbol']
    params = queries[1:]
    my_data = comp.history(period='1y')
    
    if 'Volume' in params:
        params.remove('Volume')
        my_data = my_data[['Open', 'High', 'Low', 'Close', 'Volume']]
    else:
        my_data = my_data[['Open', 'High', 'Low', 'Close']]

    if (len(params) != 0):
        for p in params:
            url_arr = urls[p]
            url = url_arr[0] + sym + url_arr[1]
            r = requests.get(url)
            d = r.json()
            df = pd.json_normalize(d, max_level=2).T
            df = df[meta:]
            df = df.iloc[::-1]
            df = df[len(df) - len(my_data):]
            my_data[p] = df.iloc[:,0].values

    data = my_data.copy()

    data5 = pd.DataFrame()
    for i in range(1,number_of_past_days+1):
        data = data.shift(1,fill_value=0).add_suffix(i)
        data5 = pd.concat([data5, data], axis = 1)

    data = yf.Ticker(sym).history(period=period_of_time)[['Open', 'Close']]

    data5['Open'] = comp.history(period=period_of_time)['Open']
    data5['target_value'] = data.apply(lambda row: row.Close - row.Open, axis=1)
    data5['target_classifier'] = data5.apply(lambda row: 1 if(row.target_value > margin) else 0, axis = 1)

    data5 = data5.shift(-(number_of_past_days))
    data5.drop(data5.tail(number_of_past_days).index, inplace=True)

    y = data5['target_classifier']
    x = data5.drop(['target_classifier','target_value'],axis=1)
    train_raw, test_raw, target, target_test = train_test_split(x,y, test_size=0.25, random_state=0)

    pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])

    #Transform raw data 
    train = pipeline.fit_transform(train_raw)
    test = pipeline.transform(test_raw)

    lr = LogisticRegression(penalty='l1',max_iter=1000, solver="liblinear")
    lr.fit(train,target)
    predicted = lr.predict(test)

    accuracy = sklearn.metrics.accuracy_score(target_test,predicted)
    tomorrow_pred = lr.predict(x[len(x)-1:])
            
    today = my_data[len(my_data) - 1:]
    today = today\
        .assign(Name = comp.info['shortName'])\
        .assign(Symbol = '(' + sym + ')')\
        .assign(Accuracy = accuracy)\
        .assign(Prediction = tomorrow_pred)

    today_json = today.to_json(orient='records')
    print(today_json, file=sys.stdout)
    

if __name__ == '__main__':
    main()