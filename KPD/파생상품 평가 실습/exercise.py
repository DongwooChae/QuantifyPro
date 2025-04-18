import numpy as np
import pandas as pd

# 3.1 배열 생성의 기초
# numpy에서 배열은 ndarray(n-dimensional array)의 약자이다.
one_dimension_ndarray = np.array([1,2,3,4])
# print(one_dimension_ndarray)

two_dimension_ndarray = np.array([[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]])
# print(two_dimension_ndarray)

# 3.2 배열생성 - ones, zeros, random
ones_two_dimension_ndarray = np.ones([3,6])
# print(ones_two_dimension_ndarray)

random_two_dimension_ndarray = np.random.rand(3,6)
print(random_two_dimension_ndarray)