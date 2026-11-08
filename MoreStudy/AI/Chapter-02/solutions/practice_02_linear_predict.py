"""Practice 02 — 모범답안."""
import numpy as np


def predict_linear(X, weights, bias):
    X = np.asarray(X, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if X.ndim != 2 or weights.ndim != 1 or X.shape[1] != weights.size:
        raise ValueError("X의 열 수와 weights의 길이가 일치해야 합니다.")
    if not (np.isfinite(X).all() and np.isfinite(weights).all() and np.isfinite(float(bias))):
        raise ValueError("모든 입력은 유한한 숫자여야 합니다.")
    return X @ weights + float(bias)


if __name__ == "__main__":
    print(predict_linear([[2, 1], [4, 0]], [3, 2], 1))
