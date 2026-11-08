"""Practice 03 — 단일 Feature 선형 모델을 한 번 갱신합니다."""
import numpy as np


def gradient_step(x, y, weight, bias, learning_rate):
    """MSE의 평균 기울기를 사용하여 (new_weight, new_bias)를 반환합니다."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.shape != y.shape or x.size == 0:
        raise ValueError("x, y는 길이가 같은 비어 있지 않은 배열이어야 합니다.")
    if not (0 < learning_rate <= 1):
        raise ValueError("learning_rate는 0보다 크고 1 이하여야 합니다.")
    # TODO: 예측, 오차, 두 기울기, 갱신된 매개변수를 계산하세요.
    raise NotImplementedError


if __name__ == "__main__":
    print(gradient_step([0, 1, 2, 3], [1, 3, 5, 7], 0, 0, .02))
