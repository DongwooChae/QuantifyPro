import pandas as pd
import numpy as np

# 모든 float64 컬럼을 정수 형태(소수점 없이)로, 천 단위마다 콤마 찍어서 출력
pd.options.display.float_format = '{:,.2f}'.format

# loader
df = pd.read_excel('costdata.xlsm', sheet_name=0, index_col='기업')

# int to float
df['고정비'] = df['고정비'].astype('float')

# 전처리를 위한 점검
print(df.isnull().sum()) # Check for missing values
print(df.dtypes) # Check data types
print(df.info())
print(df.describe())

# 추가 열 생성
df['매출원가율'] = df['매출원가'] / df['매출']
df['변동비율'] = df['변동비'] / df['매출']
df['고정비율'] = df['고정비'] / df['매출']
df['invsales'] = 1 / df['매출']
# 매출 규모 수준으로 뿌려보기
print(df.sort_values(by='매출', ascending=False))
# 이렇게 보면 매출이 가장 높은 기업은 8,756,413인데 가장 낮은 기업은 8,945로 규모 차이가 매우 큼

# qcut(사분위수 기준으로 구간을 나누어 범주화) => 이건 각 사분위별로 구간을 균등 분할함
# df['qcut'] = pd.qcut(df['매출'], 4, labels=['1', '2', '3', '4'])
# print(df['qcut'].value_counts())
# print(df.groupby('qcut')['매출'].mean())

# cut(수치를 기준으로 구간을 나누어 범주화)
df['cut'] = pd.cut(df['매출'], bins=[0, 100000, 500000, 1000000, 5000000, 10000000], labels=['1', '2', '3', '4', '5'])
print(df.sort_values(by='cut', ascending=False))
print(df['cut'].value_counts())
# 매출 백만 이하까지의 기업이 11+8+3 =22개 기업으로 전체 30개 기업 데이터 중 73%를 차지함
# cut4 카테고리(1백만~5백만) 기업이 7개에 해당, 이 구간의 기업도 유의미한 자료라고 볼 수 있음
# 따라서 매출 1백만 이하의 기업 원가율, 매출 1~5백만 구간의 원가율을 비교해보면 좋을 듯

