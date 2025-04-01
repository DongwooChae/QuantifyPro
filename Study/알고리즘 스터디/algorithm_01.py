# 1부터 n까지 연속한 숫자의 합을 구하는 알고리즘 1
# 입력 : n
# 출력 : 1부터 n까지 연속한 숫자의 합

def sum_n(n):
    s = 0
    for i in range(1, n+1):
        s = s + i
    return s

# print(sum_n(10))
# print(sum_n(100000))


def sum_square(n):
    s = 0
    for i in range(1, n+1):
        s = s + i**2 # i**2가 i의 제곱을 의미
    return s

# 제곱을 계산하려면 s + i**2로 바꿔야 함

print(sum_square(10))