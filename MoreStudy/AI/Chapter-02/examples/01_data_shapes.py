"""샘플·Feature·Target의 배열 구조를 확인합니다."""
import numpy as np

X = np.array([[2.0, 1.0], [4.0, 0.0], [6.0, 2.0]], dtype=float)
y = np.array([9.0, 17.0, 27.0], dtype=float)

print("X shape:", X.shape)  # (3, 2)
print("y shape:", y.shape)  # (3,)
print("첫 Sample:", X[0])
print("첫 Target:", y[0])
