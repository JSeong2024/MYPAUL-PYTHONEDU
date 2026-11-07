"""Exercise 04 — 결측 표식과 범위 오류를 NaN으로 바꾸고 평균 계산."""
import numpy as np

def clean_and_mean(readings: np.ndarray) -> tuple[np.ndarray, float]:
    """유효 범위 0~45°C, 결측 표식 -999. 전부 무효면 ValueError."""
    # TODO: 결측·범위 초과·비유한 수를 검사하는 마스크를 만듭니다.
    # TODO: np.where로 무효값을 np.nan으로 치환합니다.
    # TODO: 무효값이 아닌 온도 평균을 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    cleaned, mean = clean_and_mean(np.array([20, -999, 25, 48, 30]))
    print(cleaned, mean)
