"""Solution 03 — Broadcasting으로 센서별 오차 보정."""
import numpy as np

def calibrate(readings: np.ndarray, offsets: np.ndarray) -> np.ndarray:
    values = np.asarray(readings, dtype=np.float64)
    corrections = np.asarray(offsets, dtype=np.float64)
    if values.ndim != 2 or corrections.ndim != 1 or values.shape[1] != corrections.size:
        raise ValueError("입력 크기가 맞지 않습니다.")
    return values + corrections

if __name__ == "__main__":
    readings = np.array([[20.0, 21.0, 22.0], [23.0, 24.0, 25.0]])
    print(calibrate(readings, np.array([0.5, -0.5, 1.0])))
