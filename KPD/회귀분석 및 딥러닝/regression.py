import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
df = pd.read_excel('costdata.xlsm', sheet_name=0)

# 매출과 매출원가 선형회귀 분석

sales = np.array(df['매출']).reshape(-1, 1) # x축 데이터인 매출액을 2차원 배열로 변환
cost = np.array(df['매출원가'])
# cost = np.array(df['매출원가']).reshape(-1, 1) y축 데이터는 변환하지 않음


model = LinearRegression().fit(sales, cost)
print(model.score(sales, cost))  # R^2 score
print(model.intercept_) # b값
print(model.coef_) # a값

print(model.predict([[1250000]])) # 매출 1250000일 때 예측되는 매출원가



# 예측할 매출액을 변수에 담고, 2차원 배열로 준비
준비한매출액 = 1250000
예측배열 = model.predict([[준비한매출액]])

# 예측 수행
계산된원가 = 예측배열[0]

# 원가율 계산
원가율 = 계산된원가 / 준비한매출액

# 결과 출력
print("회귀분석을 통한 결과는 다음과 같습니다.")
print(f"매출액이 {준비한매출액:,}일 경우, 매출원가는 {계산된원가:,.0f}으로 산출됩니다.")
print(f"따라서 매출원가율은 {원가율:.2%}입니다.")