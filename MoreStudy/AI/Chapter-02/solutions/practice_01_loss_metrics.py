"""Practice 01 — 모범답안."""
import numpy as np


def calculate_errors(y_true, y_pred):
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)
    if actual.ndim != 1 or predicted.ndim != 1 or actual.size == 0 or actual.shape != predicted.shape:
        raise ValueError("같은 길이의 비어 있지 않은 1차원 배열을 입력하세요.")
    if not (np.isfinite(actual).all() and np.isfinite(predicted).all()):
        raise ValueError("모든 입력은 유한한 숫자여야 합니다.")
    errors = predicted - actual
    mae = float(np.mean(np.abs(errors)))
    mse = float(np.mean(errors ** 2))
    return mae, mse


if __name__ == "__main__":
    print(calculate_errors([3, 5, 7], [2, 7, 8]))
