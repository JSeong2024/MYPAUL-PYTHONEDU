"""Mini Project 02 — 선형 모델을 Gradient Descent로 학습합니다."""
import numpy as np


def gradient_descent(x: np.ndarray, y: np.ndarray, learning_rate: float = 0.05,
                     steps: int = 250):
    """(weight, bias, losses)를 반환합니다."""
    # STEP 1: weight, bias를 0으로 초기화합니다.
    # STEP 2: 예측과 MSE 기울기를 계산합니다.
    # STEP 3: learning_rate만큼 weight, bias를 갱신합니다.
    # STEP 4: 갱신한 매개변수의 MSE를 losses에 기록합니다.
    raise NotImplementedError


if __name__ == "__main__":
    x = np.linspace(-2, 2, 41)
    y = 1.5 * x + 2.8
    print(gradient_descent(x, y))
