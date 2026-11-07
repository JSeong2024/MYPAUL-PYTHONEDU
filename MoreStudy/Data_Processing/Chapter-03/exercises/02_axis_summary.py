"""Exercise 02 — 행·열별 평균 계산."""
import numpy as np

def summarize(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(행별 평균, 열별 평균)을 반환합니다."""
    # TODO: 2차원·비어 있지 않은 배열인지 확인합니다.
    # TODO: mean(axis=1), mean(axis=0)을 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    scores = np.array([[80, 90, 100], [60, 75, 90]])
    print(summarize(scores))
