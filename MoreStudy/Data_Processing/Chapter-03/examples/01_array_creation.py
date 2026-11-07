"""Python 시퀀스와 NumPy 생성 함수를 이용한 배열 만들기."""
import numpy as np

integers = np.array([10, 20, 30], dtype=np.int64)
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print("정수 배열:", integers)
print("2차원 배열:\n", matrix, sep="")
print("영행렬:\n", np.zeros((2, 3), dtype=int), sep="")
print("연속 값:", np.arange(0, 10, 2))
print("균등 간격:", np.linspace(0, 1, 5))
