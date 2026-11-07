"""조건부 선택, 결측 표식 처리, np.where()."""
import numpy as np

temperatures = np.array([22.5, -999.0, 31.2, 47.0, 25.0])
missing = temperatures == -999.0
in_range = (temperatures >= 0) & (temperatures <= 45)
valid = ~missing & in_range

cleaned = np.where(valid, temperatures, np.nan)
print("유효 데이터:", temperatures[valid])
print("제외 개수:", np.count_nonzero(~valid))
print("정제 배열:", cleaned)
print("유효 데이터 평균:", round(float(np.nanmean(cleaned)), 2))
print("30도 초과:", temperatures[valid & (temperatures > 30)])
