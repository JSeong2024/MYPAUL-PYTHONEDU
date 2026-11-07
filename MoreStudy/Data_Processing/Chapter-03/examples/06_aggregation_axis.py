"""axis별 평균·합계 및 NaN을 제외한 집계."""
import numpy as np

scores = np.array([[80.0, 90.0, 70.0],
                   [85.0, 75.0, 95.0]])
print("전체 평균:", scores.mean())
print("열별 평균(axis=0):", scores.mean(axis=0))
print("행별 평균(axis=1):", scores.mean(axis=1))
print("열별 합계:", scores.sum(axis=0))

with_missing = np.array([21.0, np.nan, 25.0])
print("NaN 제외 평균:", np.nanmean(with_missing))
print("행 평균 유지 차원:", scores.mean(axis=1, keepdims=True).shape)
