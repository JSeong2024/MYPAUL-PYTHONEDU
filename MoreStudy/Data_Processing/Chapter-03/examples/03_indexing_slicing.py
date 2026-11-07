"""2차원 배열의 인덱싱과 슬라이싱."""
import numpy as np

scores = np.array([[80, 90, 70, 100],
                   [75, 85, 95,  90],
                   [88, 92, 84,  96]])
print("두 번째 학생:", scores[1])
print("세 번째 과목:", scores[:, 2])
print("앞의 두 학생 / 두 과목:\n", scores[:2, :2], sep="")
print("선택된 두 값:", scores[[0, 2], [1, 3]])
