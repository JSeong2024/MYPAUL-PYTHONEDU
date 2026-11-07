"""자료형과 메모리, 변환, 부동소수점 비교 주의."""
import numpy as np

small = np.array([1.1, 2.2, 3.3], dtype=np.float32)
wide = small.astype(np.float64)
print("float32 bytes:", small.nbytes)
print("float64 bytes:", wide.nbytes)
print("float32 -> float64:", wide.dtype)

value = np.float64(0.1) + np.float64(0.2)
print("0.1 + 0.2 == 0.3:", value == 0.3)
print("isclose:", bool(np.isclose(value, 0.3)))
print("int16 범위:", np.iinfo(np.int16).min, np.iinfo(np.int16).max)
