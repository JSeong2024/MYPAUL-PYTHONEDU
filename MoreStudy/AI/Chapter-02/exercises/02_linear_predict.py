"""Practice 02 — 여러 Feature를 가진 선형 모델의 예측을 구현합니다."""
import numpy as np


def predict_linear(X, weights, bias):
    """shape (n_samples, n_features) -> shape (n_samples,)."""
    X = np.asarray(X, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if X.ndim != 2 or weights.ndim != 1 or X.shape[1] != weights.size:
        raise ValueError("X의 열 수와 weights의 길이가 일치해야 합니다.")
    # TODO: X @ weights + bias를 계산하세요.
    raise NotImplementedError


if __name__ == "__main__":
    print(predict_linear([[2, 1], [4, 0]], [3, 2], 1))
