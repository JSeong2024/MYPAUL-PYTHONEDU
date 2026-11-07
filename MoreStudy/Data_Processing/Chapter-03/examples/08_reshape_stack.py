"""형태 변경, 축 교환, 배열 이어 붙이기 및 쌓기."""
import numpy as np

values = np.arange(1, 7)
matrix = values.reshape(2, 3)
print("reshape:\n", matrix, sep="")
print("transpose:\n", matrix.T, sep="")

first = np.array([10, 20])
second = np.array([30, 40])
print("concatenate:", np.concatenate([first, second]))
print("stack:\n", np.stack([first, second]), sep="")
