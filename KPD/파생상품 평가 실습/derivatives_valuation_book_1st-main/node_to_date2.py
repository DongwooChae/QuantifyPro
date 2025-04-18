# 노드간격기반으로 노드별 날짜리스트 구하기

import pandas as pd
import numpy as np
import math as math

interval = 7 #1개 노드 step당 7일 간격
start_date_str = "2024-12-31" # 평가기준일
end_date_str = "2030-12-31" # 만기일

freq = f"{interval}D"
start_date = np.datetime64(start_date_str, "D")
end_date = np.datetime64(end_date_str, "D")

date_range = pd.date_range(
    start = start_date,
    end = end_date,
    freq = freq
)

date_range = pd.date_range(
    start = start_date,
    end = end_date,
    freq = freq
)

date_array = np.array(date_range)

# 만약 마지막 일자가 간격이 맞지 않아 생성되지 않은 경우, 마지막 일자를 마지막 노드에 추가하기
if date_array[-1]!= end_date:
    date_array = np.append(date_array, end_date)

print(date_array)
