"""Coding Practice 02 — 정확도와 희귀 클래스 재현율을 계산합니다."""
import numpy as np


def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    # TODO: 전체 정확도와 클래스 1(드문 사건) 재현율을 순서대로 반환합니다.
    # TODO: 실제 클래스 1이 없는 경우에는 재현율을 None으로 반환합니다.
    raise NotImplementedError("TODO: evaluate")


if __name__ == "__main__":
    true = np.array([0, 0, 1, 0, 1, 0])
    predicted = np.array([0, 0, 0, 0, 1, 0])
    print(evaluate(true, predicted))  # 예상 결과: (0.8333..., 0.5)
