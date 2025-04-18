import pandas as pd
import numpy as np
import math

# 파이썬을 통해 이자율 부트스트래핑을 할 수 있으며, YTM에서 현물이자율, 선도이자율을 산출하는 과정을 다룬다.
# 이자지급주기는 1년을 가정하고, 관측되는 YTM의 기간은 1년, 3년, 5년물이며 각각의 YTM은 1%, 3%, 5%로 가정한다.
# 부트스트래핑의 과정은 관측되는 YTM의 이자지급주기에 따라서, 관측되지 않는 기간에 대한 YTM 수익률은 보간법을 통해 산출하고
# 각 기간에 산출된 YTM을 통해서 현물이자율을 산출하고, 각 산출된 현물이자율을 이용해서 선도이자율을 산출한다.

# Step1 YTM 보간법

basis = 1 # 이자지급주기
ytm_periods = [1,3,5] # 관측되는 YTM의 기간
ytm_interests = [0.01, 0.03, 0.03]
bond_principal = 100 # 채권이자원금

# basis마다 노드 생성
basis_array = np.arange(basis, 5+basis, basis)
# 출력 : [1, 2, 3, 4, 5]

# ytm 보간법
interpolated_ytm_interests = np.interp(basis_array, ytm_periods, ytm_interests)
# 출력 : [0.01, 0.02, 0.03, 0.04, 0.05]

# numpy의 interp 함수를 통해 YTM이 관측되지 않는 2년, 4년에 대해 보간법을 통해 이자율을 채워준다.

# Step2 현물이자율 구하기
spot_rates = [interpolated_ytm_interests[0]] # 첫 번째 현물이자율은 ytm 관측이자율로 고정

for idx, ytm in enumerate(interpolated_ytm_interests[1:]):
    t = (idx+1)*basis

    # 이자의 현재가치 변수 초기화
    pv_interest = 0
    # 이자지급주기마다 이자 현재가치 계산
    for j in range(idx+1):

        current_interest = bond_principal*basis*ytm
        exponent = j+1

        # 기간에 대응하는 현물이자율로 원금이자를 할인하여 이자의 현재가치 계산
        pv_current_interest = current_interest / np.power((1+spot_rates[j]), exponent)

        # 이자누적
        pv_interest += pv_current_interest

    # 만기원리금 계산 : 원금 + (1+ytm*basis)
    total_interest_principal = bond_principal *(1+ytm)

    # 만기원리금의 현재가치
    pv_bond_price = bond_principal - pv_interest

    exponent = idx+2
    pv_factor = total_interest_principal / pv_bond_price
    spot_rate = (np.power(pv_factor, 1/exponent)-1)

    spot_rates.append(spot_rate)

# Step3. 선도이자율 구하기
forward_rates = [spot_rates[0]]
for i in range(1, len(spot_rates)):
    t1 = i+1
    t2 = i
    forward_rate = ((np.power((1+spot_rates[i]), t1) / np.power((1+spot_rates[i-1]), t2))-1)
    forward_rates.append(forward_rate)



