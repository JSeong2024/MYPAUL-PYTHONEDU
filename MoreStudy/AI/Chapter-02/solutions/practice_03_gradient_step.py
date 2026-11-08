"""Practice 03 — 모범답안."""
import numpy as np


def gradient_step(x, y, weight, bias, learning_rate):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.shape != y.shape or x.size == 0:
        raise ValueError("x, y는 길이가 같은 비어 있지 않은 배열이어야 합니다.")
    if not (0 < learning_rate <= 1):
        raise ValueError("learning_rate는 0보다 크고 1 이하여야 합니다.")
    if not np.isfinite(x).all() or not np.isfinite(y).all() or not np.isfinite([weight, bias, learning_rate]).all():
        raise ValueError("모든 입력은 유한한 숫자여야 합니다.")
    error = weight * x + bias - y
    grad_weight = 2.0 * float(np.mean(error * x))
    grad_bias = 2.0 * float(np.mean(error))
    return (float(weight - learning_rate * grad_weight),
            float(bias - learning_rate * grad_bias))


if __name__ == "__main__":
    print(gradient_step([0, 1, 2, 3], [1, 3, 5, 7], 0, 0, .02))
