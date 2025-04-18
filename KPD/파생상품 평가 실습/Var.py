import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import math

# cost_price = yf.download('COST', start = '2011-01-01', end = '2025-04-10')
# print(cost_price.head(5))

# 분석할 티커 리스트
tickers = ['COST', 'AAPL', 'MSFT', 'NVO','CTAS','ATCO-A.ST']

# 여러 티커 데이터를 한 번에 다운로드
data = yf.download(tickers, start='2011-01-01', end='2025-04-10')

# 여기서 data는 MultiIndex 구조로 반환됨.
# auto_adjust가 True이므로, "Close" 열이 이미 조정된 가격임.
price_df = data['Close']  # 인덱스: 날짜, 컬럼: 티커
price_df = price_df.sort_index(ascending=False)  # 날짜를 내림차순으로 정렬

# print(price_df.head(30))

# 주가의 로그 수익률 계산
# 로그 수익률 = ln(P_t / P_{t-1})
log_returns = np.log(price_df / price_df.shift(1))

# 결측값은 첫 행 때문에 발생하므로 제거
log_returns = log_returns.dropna()

# 결과 확인
# print(log_returns.head(10))

# 개별 기업의 일일 변동성(표준편차) 계산
# daily_volatility = log_returns.std()
# print("\n각 티커별 일일 변동성 (표준편차):")
# print(daily_volatility)

# 월별 표준편차 계산
# 월별로 재샘플하고 각 월의 표준편차 계산
# monthly_volatility = log_returns.resample('M').std()

# print("월별 표준편차(변동성) 데이터:")
# print(monthly_volatility.head(10))

# 2024-01-01 ~ 2025-04-09 주가 데이터를 활용한 VaR 계산
# 일일 통계량 계산
mu_daily = log_returns.mean()
sigma_daily = log_returns.std()

# 60일로 시간 확장
T = 120
mu_60 = mu_daily * T
sigma_60 = sigma_daily * np.sqrt(T)

# VaR 계산
z_95 = 1.645
z_99 = 2.326

var_60_95 = 1 - np.exp(mu_60 - z_95 * sigma_60)
var_60_99 = 1 - np.exp(mu_60 - z_99 * sigma_60)

var_df =pd.DataFrame({
    'Var_60_95' : var_60_95,
    'Var_60_99' : var_60_99
})

print(var_df)
print(log_returns.head(30))
print("일일 로그 수익률의 평균:", mu_daily)
print("일일 로그 수익률의 표준편차:", sigma_daily)

# 누적 로그수익률 계산하기
price_df_ascending = price_df.sort_index(ascending=True)  # 날짜를 오름차순으로 정렬

log_returns = np.log(price_df_ascending / price_df_ascending.shift(1))
log_returns = log_returns.dropna()

# 2024년 이후 데이터만 선택
log_returns_2024 = log_returns.loc['2024-01-01':]
accumulated_growth_factor = np.exp(log_returns_2024.sum())
cumulative_return = accumulated_growth_factor - 1
print("2024년 이후 단순 누적 수익률 (로그 기반)", cumulative_return)


# 단순 수익률 계산을 통한 검증

start_date = pd.Timestamp("2024-01-02")
# asof는 정렬된 인덱스에서 지정한 날짜에 가장 가까운 이전 값을 찾아준다.
closest_date = price_df_ascending.index.asof(start_date)

print("실제 사용된 시작 날짜:", closest_date)
end_date = price_df_ascending.index[-1] 

p_start = price_df_ascending.loc[closest_date]
p_end = price_df_ascending.loc[end_date]

simple_return = (p_end - p_start) / p_start
print(f"기준일 : {closest_date}, 최신일 :{end_date}")
print("단순 수익률:", simple_return)

# 각 티커별로 기준일과 최신일의 주가 추출
# 날짜를 문자열로 변환 (ex: '2024-01-02', '2025-04-09')
p_start_date_str = str(closest_date.date())
p_end_date_str = str(end_date.date())

# DF 생성
p_df = pd.DataFrame({
    f"{p_start_date_str}": p_start[tickers].values,
    f"{p_end_date_str}": p_end[tickers].values
}, index=tickers)

print(p_df)