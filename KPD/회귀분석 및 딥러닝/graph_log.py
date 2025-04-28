import pandas as pd
import numpy as np
import mplcursors
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator , StrMethodFormatter
df = pd.read_excel('costdata.xlsm', sheet_name=0)


# 1) 0이 아닌, 양수인 데이터만 골라오기
mask = (df['매출'] > 0) & (df['매출원가'] > 0)
sales_pos = df.loc[mask, '매출'].values
cost_pos  = df.loc[mask, '매출원가'].values

fig, ax = plt.subplots(figsize=(4,4))
sc = ax.scatter(sales_pos, cost_pos, color='royalblue', alpha=0.7)

ax.set_xscale('log')   # x축을 로그 스케일로
ax.set_yscale('log')   # y축도 로그 스케일로

ax.set_xlabel('Sales')
ax.set_ylabel('Cost')

# 로그스케일 눈금 찍는 구간 추가
ax.xaxis.set_major_locator(LogLocator(base=10.0,subs=[1,2,5]  , numticks=10))
ax.yaxis.set_major_locator(LogLocator(base=10.0,subs=[1,2,5]  , numticks=10))

# 천 단위 콤마 포맷 (로그축에서도 작동)
ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

# hover= True로 설정하면 마우스 오버 시 데이터 포인트에 대한 정보 표시
mplcursors.cursor(sc, hover=True).connect(
    "add", lambda sel: sel.annotation.set_text(
        f"Sales: {sel.target[0]:,.0f}\nCost : {sel.target[1]:,.0f}"
    )
)


ax.grid(True, which='both', ls='--', lw=0.5)
plt.tight_layout()
plt.show()
