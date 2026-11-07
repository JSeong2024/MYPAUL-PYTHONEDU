"""Exercise 03 — Broadcasting으로 센서별 오차 보정."""
import numpy as np

def calibrate(readings: np.ndarray, offsets: np.ndarray) -> np.ndarray:
    """열마다 대응하는 보정값을 더한 새 배열을 반환합니다."""
    # TODO: readings는 2차원, offsets는 열 개수와 같은 길이의 1차원입니다.
    # TODO: 입력 shape가 다르면 ValueError를 발생시킵니다.
    # TODO: Broadcasting을 사용해 결과를 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    readings = np.array([[20.0, 21.0, 22.0], [23.0, 24.0, 25.0]])
    print(calibrate(readings, np.array([0.5, -0.5, 1.0])))
