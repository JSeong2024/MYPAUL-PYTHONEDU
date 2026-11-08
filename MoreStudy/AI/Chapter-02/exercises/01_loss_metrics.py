"""Practice 01 — MAE와 MSE를 구현합니다."""
import numpy as np


def calculate_errors(y_true, y_pred):
    """(MAE, MSE)를 반환합니다. 입력은 같은 길이의 1차원 수치 배열입니다."""
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)
    if actual.ndim != 1 or predicted.ndim != 1 or actual.size == 0 or actual.shape != predicted.shape:
        raise ValueError("같은 길이의 비어 있지 않은 1차원 배열을 입력하세요.")
    # TODO: error, mae, mse를 계산하세요.
    raise NotImplementedError


if __name__ == "__main__":
    print(calculate_errors([3, 5, 7], [2, 7, 8]))
