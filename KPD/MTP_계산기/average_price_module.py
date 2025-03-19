import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display
import os
import import_ipynb
import plotly
import matplotlib

# Raw data URL 정의
industry_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/00.%ED%91%9C%EC%A4%80%EC%82%B0%EC%97%85%EB%B6%84%EB%A5%98.xlsx?raw=true'
price_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/01_%EC%A3%BC%EA%B0%80.xlsx?raw=true'
value_per_stock_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/02_%EC%A3%BC%EB%8B%B9%EA%B0%80%EC%B9%98.xlsx?raw=true'
fsdata_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/03_%EC%9E%AC%EB%AC%B4%EB%8D%B0%EC%9D%B4%ED%84%B0.xlsx?raw=true'

# 데이터 불러오기 함수
def load_data():
    industry = pd.read_excel(industry_url, index_col='종목명')
    price = pd.read_excel(price_url, parse_dates=['Date'], index_col='Date')
    value_per_stock = pd.read_excel(value_per_stock_url, index_col=0)
    fsdata = pd.read_excel(fsdata_url)
    return industry, price, value_per_stock, fsdata

# 평균주가와 가치배수 계산 함수
def calculate_valuation(valuation_date, start_date, end_date):
    _, price, value_per_stock, _ = load_data()

    # 평균 주가 계산
    selected_price = price.loc[start_date:end_date]
    average_price = selected_price.mean()
    df_average_price = pd.DataFrame([average_price], index=[f'{start_date} ~ {end_date}'])

    # value_per_stock 데이터 업데이트
    value_per_stock['평균주가'] = value_per_stock.index.map(df_average_price.loc[f'{start_date} ~ {end_date}'])

    # 가치배수 계산
    value_per_stock['PER'] = value_per_stock['평균주가'] / value_per_stock['EPS']
    value_per_stock['PBR'] = value_per_stock['평균주가'] / value_per_stock['BPS']
    value_per_stock['PSR'] = value_per_stock['평균주가'] / value_per_stock['SPS']

    return value_per_stock
