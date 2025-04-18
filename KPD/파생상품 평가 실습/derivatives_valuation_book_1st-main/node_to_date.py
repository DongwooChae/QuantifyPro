import numpy as np
import math as math
import pandas as pd

# 노드개수기반으로 노드별 날짜리스트 구하기

# input 정의
start_date_str = "2024-12-31" # 평가기준일
end_date_str = "2030-12-31" # 만기일
node_count = 30 # 노드 개수

start_date = pd.Timestamp(start_date_str)
end_date = pd.Timestamp(end_date_str)

date_range = pd.date_range(
    start=start_date,
    end=end_date,
    periods = node_count)

date_array = np.array(date_range)

print(date_array)