"""Solution 04 — 결측 표식과 범위 오류를 NaN으로 바꾸고 평균 계산."""
import numpy as np

def clean_and_mean(readings: np.ndarray) -> tuple[np.ndarray, float]:
    values = np.asarray(readings, dtype=np.float64)
    valid = (values != -999) & np.isfinite(values) & (values >= 0) & (values <= 45)
    if not np.any(valid):
        raise ValueError("유효한 측정값이 없습니다.")
    clean = np.where(valid, values, np.nan)
    return clean, float(np.nanmean(clean))

if __name__ == "__main__":
    cleaned, mean = clean_and_mean(np.array([20, -999, 25, 48, 30]))
    print(cleaned, mean)
