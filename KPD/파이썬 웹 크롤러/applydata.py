import pandas as pd
import openpyxl as xl

raw = pd.read_excel('product.xlsx', engine="openpyxl")



# 1. mask 생성
mask = raw['상품목록'] == '7102 Metal Chair'

# 2. loc의 두 인자 방식으로 할당 - 원본에 바로 반영
raw.loc[mask, '카테고리'] = '의자'

raw.loc[(raw['상품목록'] == 'Wooden Table 34'), '카테고리'] = '테이블'
print(raw)