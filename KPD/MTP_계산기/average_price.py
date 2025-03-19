import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython.display import display
import os
import import_ipynb
import plotly
import matplotlib

# Raw_data 추출

industry_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/00.%ED%91%9C%EC%A4%80%EC%82%B0%EC%97%85%EB%B6%84%EB%A5%98.xlsx?raw=true'
price_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/01_%EC%A3%BC%EA%B0%80.xlsx?raw=true'
value_per_stock_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/02_%EC%A3%BC%EB%8B%B9%EA%B0%80%EC%B9%98.xlsx?raw=true'
fsdata_url = 'https://github.com/DongwooChae/QuantifyPro/blob/master/KPD/03_%EC%9E%AC%EB%AC%B4%EB%8D%B0%EC%9D%B4%ED%84%B0.xlsx?raw=true'

industry = pd.read_excel(industry_url, index_col = '종목명')
price = pd.read_excel(price_url, parse_dates=['Date'], index_col='Date')
value_per_stock = pd.read_excel(value_per_stock_url, index_col=0)
fsdata = pd.read_excel(fsdata_url)


# 평가기준일 입력받기
valuation_date = input("평가기준일을 입력하세요 (예: 2023-06-30): ")

# 평균 주가를 계산할 기간의 시작일과 종료일 입력받기
start_date = input("평균 주가를 계산할 기간의 시작일을 입력하세요 (예: 2023-01-01): ")
end_date = input("평균 주가를 계산할 기간의 종료일을 입력하세요 (예: 2023-06-30): ")

# 입력한 기간 동안의 데이터를 선택
selected_price = price.loc[start_date:end_date]

# 주가 데이터의 평균 계산(.mean 메서드 사용)
average_price = selected_price.mean()

# 평균값으로 구성된 데이터프레임 생성, 인덱스 이름 설정
df_average_price = pd.DataFrame([average_price], index=[f'{start_date} ~ {end_date}'])

# value_per_stock 데이터프레임에 '평균주가' 열 추가하여 값 매핑하기
value_per_stock['평균주가'] = value_per_stock.index.map(df_average_price.loc[f'{start_date} ~ {end_date}'])

# 가치배수 계산
value_per_stock['PER'] = value_per_stock['평균주가'] / value_per_stock['EPS']
value_per_stock['PBR'] = value_per_stock['평균주가'] / value_per_stock['BPS']
value_per_stock['PSR'] = value_per_stock['평균주가'] / value_per_stock['SPS']

# print(value_per_stock.loc['삼성전자':'NAVER',['평균주가','EPS','BPS','SPS','PER','PBR','PSR']])