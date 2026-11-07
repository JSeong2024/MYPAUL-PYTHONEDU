"""서로 다른 shape의 배열을 호환 가능한 차원으로 계산."""
import numpy as np

readings = np.array([[20.0, 22.0, 24.0],
                     [19.0, 21.0, 25.0]])   # (2, 3)
offsets = np.array([0.5, -0.5, 1.0])       # (3,)
corrected = readings + offsets
print("센서별 보정:\n", corrected, sep="")

row_offsets = np.array([[0.0], [2.0]])    # (2, 1)
print("행별 추가 보정:\n", corrected + row_offsets, sep="")
print("계산 결과 shape:", np.broadcast_shapes((2, 3), (3,)))

try:
    np.broadcast_shapes((2, 3), (4,))
except ValueError:
    print("(2, 3)과 (4,)는 Broadcasting 불가")
