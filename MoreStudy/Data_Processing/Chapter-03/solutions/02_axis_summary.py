"""Solution 02 — 행·열별 평균 계산."""
import numpy as np

def summarize(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(matrix, dtype=np.float64)
    if values.ndim != 2 or 0 in values.shape:
        raise ValueError("비어 있지 않은 2차원 배열이 필요합니다.")
    return values.mean(axis=1), values.mean(axis=0)

if __name__ == "__main__":
    scores = np.array([[80, 90, 100], [60, 75, 90]])
    print(summarize(scores))
