"""슬라이싱 View와 정수 배열 인덱싱 Copy의 차이."""
import numpy as np

original = np.array([10, 20, 30, 40, 50])
view = original[1:4]
view[0] = 99
print("View 변경 후 원본:", original)
print("View 공유 여부:", np.shares_memory(original, view))

selected = original[[1, 3]]  # 고급 인덱싱: 새로운 배열
selected[0] = -1
print("고급 인덱싱 변경 후 원본:", original)
print("고급 인덱싱 공유 여부:", np.shares_memory(original, selected))

independent = original.copy()
independent[0] = -100
print("copy() 변경 후 원본:", original)
