"""ndarray의 크기, 차원, 원소 수 및 자료형 확인."""
import numpy as np

readings = np.array([[21.5, 23.0, 22.8], [24.1, 23.7, 22.0]])
print("배열:\n", readings, sep="")
print("shape:", readings.shape)
print("ndim:", readings.ndim)
print("size:", readings.size)
print("dtype:", readings.dtype)
print("itemsize:", readings.itemsize)
print("nbytes:", readings.nbytes)
