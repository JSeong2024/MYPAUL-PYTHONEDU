"""Coding Practice 02 — 정답 구현."""
import numpy as np


def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float | None]:
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    if y_true.ndim != 1 or y_true.size == 0 or y_true.shape != y_pred.shape:
        raise ValueError("정답과 예측이 같은 길이의 비어 있지 않은 배열이어야 합니다.")
    accuracy = float(np.mean(y_true == y_pred))
    positives = y_true == 1
    rare_recall = float(np.mean(y_pred[positives] == 1)) if positives.any() else None
    return accuracy, rare_recall


if __name__ == "__main__":
    print(evaluate(
        np.array([0, 0, 1, 0, 1, 0]), np.array([0, 0, 0, 0, 1, 0]),
    ))
