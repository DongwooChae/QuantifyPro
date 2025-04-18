# step1 날짜 배열 생성
# step2 부트스트래핑을 사용하여 kd 및 rf spot rate 및 forward rate 계산
# step3 상환전환우선주 상환금액 트리 생성(주계약/풋)
# step4 주가이항트리 생성
# step5 GS Valuation(Pay off)
# step6 엑셀로 결과 추출

# Step0 : Input 값 정의
import numpy as np
import pandas as pd
import math

# input
s = 6000 # 기초자산가격
x = 7500 # 행사가격
put_yield = 0.05 # put 수익률
rf = 0.015 # 무위험이자율
kd = 0.05 # 위험이자율
volatility = 0.255 #주가변동성
delta_t = 1
u = np.exp(volatility*np.sqrt(delta_t)) # 상승계수
d = 1/u # 하락계수
p = (np.exp(rf*delta_t)-d)/(u-d) # 위험중립확률
q = 1-p

# Step1 : 날짜 배열 생성


def create_date_array():
    # 평가 기준일 및 만기일을 입력받습니다.
    # 입력은 "YYYY-MM-DD" 형식으로 진행됩니다.
    start_date_str = input("평가기준일을 입력하세요 (YYYY-MM-DD): ")
    end_date_str = input("만기일을 입력하세요 (YYYY-MM-DD): ")
    
    # 노드 1개당 간격(일수) 입력 (예: 7)
    interval_days = int(input("노드 1개당 간격(일수)을 입력하세요 (예: 7): "))

    # pandas의 date_range를 이용해 날짜 배열 생성 (1년은 365일로 가정)
    date_range = pd.date_range(start=start_date_str, end=end_date_str, freq=f"{interval_days}D")
    date_array = np.array(date_range)
    
    # 마지막 날짜가 만기일과 다르면 만기일을 마지막 노드로 추가합니다.
    if date_array[-1] != pd.Timestamp(end_date_str):
        date_array = np.append(date_array, pd.Timestamp(end_date_str))
    
    return date_array


# date_array는 create_date_array() 함수를 통해 생성된 후 있다고 가정합니다.
date_array = create_date_array()
start_date = pd.Timestamp(date_array[0])
year_fraction_array = np.array([(pd.Timestamp(d) - start_date).days / 365.0 for d in date_array])

node_count = len(date_array)

# Step2 : 부트스트래핑을 사용하여 위험이자율과 rf의 현물이자율 및 선도이자율 계산

basis = 1 # 이자지급주기
# 관측된 YTM 만기와 해당 이자율
observed_maturities = [1, 3, 5 ,10] #관측된 기간(년)
observed_ytm = [0.0313, 0.0312, 0.0308, 0.0339] #관측된 YTM(연이율)

# 1년부터 10년까지 1년 단위로 만기 배열 생성
basis_array = np.arange(basis, 10 + basis, basis)
# 보간법을 이용하여 각 만기에 해당하는 YTM 산출
interpolated_ytm_interests = np.interp(basis_array, observed_maturities, observed_ytm)

# 본 예제에서는 채권의 액면가를 100으로 가정하고, 채권이 파 가격(표면가)으로 거래된다고 가정합니다.
bond_principal = 100.0

# 1년 차는 spot rate를 관측된 YTM로 가정
spot_rates = [interpolated_ytm_interests[0]]  # year 1 spot rate

# 2년 차부터 10년 차까지 부트스트래핑 진행
# (부트스트래핑의 기본 아이디어:
#  채권의 가격은 각 기간별 쿠폰의 현재가치 합과 만기 원리금의 현재가치의 합과 같아야 하므로,
#  이전에 산출된 spot rate들을 이용해 미지의 spot rate를 구함)
for idx, ytm in enumerate(interpolated_ytm_interests[1:]):
    # 현재 만기는 idx+2 (idx=0 -> 2년 차, idx=1 -> 3년 차, …)
    maturity = idx + 2

    # 각 기간의 쿠폰 지급액 (예: 액면가 * ytm, 1년 간격이므로)
    coupon = bond_principal * ytm

    # 각 조기(만기 전) 쿠폰 지급액의 현재가치 합계를 계산
    pv_coupons = 0.0
    for j in range(maturity - 1):
        # j = 0부터 maturity-2 (즉, 앞의 쿠폰 지급들)
        # j번째 쿠폰은 j+1년 후 지급되며, 이미 구한 spot_rates[j]로 할인함
        pv_coupons += coupon / (1 + spot_rates[j])**(j+1)

    # 채권은 액면가(PAR)로 거래된다고 가정하면, 채권 가격은 bond_principal 입니다.
    # 따라서, 만기 지급액(원금 + 마지막 쿠폰)의 현재가치는 다음과 같이 구해야 함:
    # bond_principal = pv_coupons + (bond_principal + coupon) / (1 + spot_rate_maturity)**maturity
    # 미지의 spot_rate_maturity를 구하면,
    # (bond_principal + coupon) / (1 + spot_rate_maturity)**maturity = bond_principal - pv_coupons
    # => 1 + spot_rate_maturity = ((bond_principal + coupon) / (bond_principal - pv_coupons))^(1/maturity)
    # => spot_rate_maturity = ((bond_principal + coupon) / (bond_principal - pv_coupons))^(1/maturity) - 1

    # 계산
    denominator = bond_principal - pv_coupons
    if denominator <= 0:
        raise ValueError("할인계산에서 분모가 0 이하입니다. 쿠폰 지급과 이전 spot rate 값들을 재확인하세요.")

    pv_factor = (bond_principal + coupon) / denominator
    spot_rate_maturity = np.power(pv_factor, 1/maturity) - 1

    spot_rates.append(spot_rate_maturity)

# Forward rates (필요 시 계산)
forward_rates = [spot_rates[0]]
for i in range(1, len(spot_rates)):
    maturity = i + 1
    prev_maturity = i
    fwd_rate = ( (1 + spot_rates[i])**maturity / (1 + spot_rates[i-1])**prev_maturity ) - 1
    forward_rates.append(fwd_rate)

# 이제 risk-free spot rate 곡선(spot_rates)을 활용합니다.
# 신용조정 할인율 곡선을 구성하기 위해, 입력 kd와 rf의 차이를 크레딧 스프레드로 가정하고 보정
credit_spread = kd - rf  # 예: 0.05 - 0.015 = 0.035
kd_spot_rates = [r + credit_spread for r in spot_rates]

# -------------------------------
# (Step3) 상환전환우선주 상환금액 및 사채가치 계산 (주계약/put)
# -------------------------------
# 기존에는 노드 인덱스를 사용하여 계산했으나, 이제 실제 연 분수(year_fraction_array)를 사용합니다.
# put 금액은 행사가격에 put 이자율을 해당 기간(연 분수)만큼 복리 반영하여 계산합니다.
put_ammount_array = x * np.power((1 + put_yield), year_fraction_array)
# print("Put Amount Array:")
# print(put_ammount_array)

# put_ammount_array와 동일한 크기의 사채 가치 배열(bond_array) 생성
bond_array = np.zeros_like(put_ammount_array)
# 마지막 노드(만기)에서는 상환금액과 동일하게 가정
bond_array[-1] = put_ammount_array[-1]

# 각 노드에서 이전 노드로 할인하면서 사채 가치를 역산 (백워드 방식)
# 할인 시에는, 각 노드 간 연차(Δt)를 고려하고, kd_spot_rates 곡선에서 해당 시점의 금리를 보간하여 사용합니다.
for i in reversed(range(node_count - 1)):
    dt = year_fraction_array[i+1] - year_fraction_array[i]  # 해당 노드의 실제 시간 차 (년 단위)
    # i+1 노드에 해당하는 kd_rate: basis_array와 kd_spot_rates에서 보간
    kd_rate = np.interp(year_fraction_array[i+1], basis_array, kd_spot_rates)
    # 할인: (1 + kd_rate)^(Δt)로 나누어 현재가치로 변환
    bond_array[i] = bond_array[i+1] / np.power(1 + kd_rate, dt)
    
print("Bond Array (Discounted Put/Redemption Values):")
print(bond_array)

# -------------------------------
# (Step4) 주가 이항트리 생성
# -------------------------------
# 날짜 배열에서 첫 두 노드 간의 시간차(연 단위)를 사용하여, 이항트리의 시간 스텝(Δt_year)을 결정
delta_t_year = year_fraction_array[1] - year_fraction_array[0]  # 고정되어 있음 (예: 7/365)
# 상승 및 하락 계수 재계산 (시간 스텝 반영)
u = np.exp(volatility * np.sqrt(delta_t_year))
d = 1 / u
# 위험중립확률 p, q: 무위험 금리 rf_input를 그대로 사용하거나, 해당 시점의 risk-free rate를 보간해 사용할 수 있음
# 여기서는 간단히 rf_input를 사용 (또는 np.exp(rf_input*delta_t_year) 사용 가능)
p = (np.exp(rf * delta_t_year) - d) / (u - d)
q = 1 - p

# n x n 주가 이항트리 생성
stock_binomial_tree = np.zeros((node_count, node_count))
stock_binomial_tree[0, 0] = s
for i in range(1, node_count):
    # 첫 행: 상승 경로
    stock_binomial_tree[0, i] = stock_binomial_tree[0, i-1] * u
    # 나머지: 하락 경로
    stock_binomial_tree[1:i+1, i] = stock_binomial_tree[:i, i-1] * d

print("Stock Binomial Tree (부분 출력):")
print(stock_binomial_tree[:3, :3])

# -------------------------------
# (Step5) GS Valuation (Pay off)
# -------------------------------
# 초기화: 의사결정 트리, 할인율 트리, GS 가치 트리, 보유 가치 트리
decision_tree = np.zeros_like(stock_binomial_tree)
discount_factor_tree = np.zeros_like(stock_binomial_tree)
gs_value_tree = np.zeros_like(stock_binomial_tree)
holding_value_tree = np.zeros_like(stock_binomial_tree)

# Step5.2: 마지막 시점 (만기)에서 의사결정: 전환 가치와 상환 가치 중 최대값 선택
gs_value_tree[:, -1] = np.maximum(stock_binomial_tree[:, -1], bond_array[-1])
# 의사결정: 전환이면 1, 상환이면 0
decision_tree[:, -1] = np.where(gs_value_tree[:, -1] == stock_binomial_tree[:, -1], 1, 0)

# 마지막 노드의 할인율: 전환 시는 risk-free (보간된 risk-free rate), 상환 시는 신용위험(rate from kd_spot_rates)
rf_last = np.interp(year_fraction_array[-1], basis_array, spot_rates)
kd_last = np.interp(year_fraction_array[-1], basis_array, kd_spot_rates)
discount_factor_tree[:, -1] = np.where(decision_tree[:, -1] == 1, rf_last, kd_last)

# Step5.3: 백워드 인덕션을 통해 이전 노드의 가치를 계산
for t in reversed(range(gs_value_tree.shape[1] - 1)):
    # 해당 시점과 t+1 노드 간의 시간 차 (년 단위)
    dt = year_fraction_array[t+1] - year_fraction_array[t]
    
    # t시점의 보유가치를 업데이트: t+1 노드에서 각각 전환과 상환의 확률로 할인
    # 할인 시 해당 노드의 할인율 값에 dt를 곱해 적용 (np.exp(- rate * dt))
    holding_value_tree[:t+1, t] = (
          gs_value_tree[:t+1, t+1] * p * np.exp(-discount_factor_tree[:t+1, t+1] * dt)
        + gs_value_tree[1:t+2, t+1] * q * np.exp(-discount_factor_tree[1:t+2, t+1] * dt)
    )
    
    # t시점에서의 RCPS 가치는 (전환 가치, 상환 가치, put 금액, 보유 가치) 중 최댓값
    gs_value_tree[:t+1, t] = np.maximum.reduce((
        stock_binomial_tree[:t+1, t], 
        np.full((t+1,), bond_array[t]),
        np.full((t+1,), put_ammount_array[t]),
        holding_value_tree[:t+1, t]
    ))
    
    # t시점 의사결정 업데이트: 전환이면 1, 상환이면 0, 아니면 미래 확률 가중치
    decision_tree[:t+1, t] = np.where(
        gs_value_tree[:t+1, t] == stock_binomial_tree[:t+1, t],
        1,
        np.where(
            gs_value_tree[:t+1, t] == put_ammount_array[t],
            0,
            decision_tree[:t+1, t+1] * p + decision_tree[1:t+2, t+1] * q
        )
    )
    
    # t시점 할인율 업데이트: 해당 노드의 연 분수에 따른 risk-free 및 kd rate를 보간하여 사용
    rf_t = np.interp(year_fraction_array[t], basis_array, spot_rates)
    kd_t = np.interp(year_fraction_array[t], basis_array, kd_spot_rates)
    discount_factor_tree[:t+1, t] = np.where(
        decision_tree[:t+1, t] == 1,
        rf_t,
        np.where(
            decision_tree[:t+1, t] == 0,
            kd_t,
            rf_t * p + kd_t * q
        )
    )

print("GS Value at initial node (0,0):", gs_value_tree[0, 0])

# -------------------------------
# (Step6) 엑셀로 결과 추출
# -------------------------------
excel_data = {
    "stock_binomial_tree": stock_binomial_tree,
    "put_ammount_array": put_ammount_array,
    "bond_array": bond_array,
    "decision_tree": decision_tree,
    "discount_factor_tree": discount_factor_tree,
    "holding_value_tree": holding_value_tree,
    "gs_value_tree": gs_value_tree,
}

excel_path = "Ch2.1_goldmanSachs.xlsx"
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    for key in excel_data.keys():
        result_df = pd.DataFrame(excel_data[key])
        result_df.to_excel(writer, sheet_name=key, index=True)