# 라이브러리 import

import pandas as pd
import numpy as np

# rawdata import

df_kosdaq_group = pd.read_excel('company.xlsx', sheet_name=0)
df_kospi_group = pd.read_excel('company.xlsx', sheet_name=1)
df_kospi_company = pd.read_excel('company.xlsx', sheet_name=2)
df_kosdaq_company = pd.read_excel('company.xlsx', sheet_name=3)
df_company = pd.read_excel('company.xlsx', sheet_name=4, index_col='종목명')

price = pd.read_excel('price.xlsx', sheet_name=0, index_col='날짜')
fsdata = pd.read_excel('fsdata_0331.xlsx', sheet_name=0, index_col='종목명')





