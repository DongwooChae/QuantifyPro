import numpy as np
import math

# 주가이항모형(주가이항트리 그리기)

# input 값
node_count = 10 # 노드 개수
u = 1.1 # 상승계수
d = 1/u # 하락계수
s = 10000 # 기초자산 주가

# 노드개수만큼의 0으로 이루어진, n x n 배열 생성
stock_bionomial_tree = np.zeros((node_count, node_count))

# 가장 첫 번째 노드에 기초자산 주가 설정
stock_bionomial_tree[0, 0]=s

for i in range(1, node_count):
    for j in range(i+1):
        #상승 계수는 i-j번, 하락계수는 j만큼 적용
        stock_bionomial_tree[j,i] = s *math.pow(u,i-j)*math.pow(d,j)

# 이항모형 실습(slicing 사용)
# 노드개수만큼의 0으로 이루어진 n x n 배열 생성
stock_binomial_tree = np.zeros((node_count, node_count))

# 가장 첫 번째 노드에 기초자산 주가 설정
stock_binomial_tree[0, 0] = s

# 두 번째 노드부터 마지막 노드까지 순차적으로 실행되는 for-loop 실행
for i in range(1, node_count):
    # 상승노드의 경우 이전 노드에서 상승계수만 반영
    stock_binomial_tree[0, i] = stock_binomial_tree[0, i-1]*u
    # 하락노드의 경우 이전 노드에서 하락계수만 반영
    stock_binomial_tree[1:i+1, i] = stock_binomial_tree[:i, i-1]*d

    