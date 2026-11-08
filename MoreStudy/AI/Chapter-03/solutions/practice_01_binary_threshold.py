"""Practice 01 모범 구현."""
import numpy as np


def predict_labels(probabilities, threshold=0.5):
    values = np.asarray(probabilities, dtype=float)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("1차원 유한한 확률 배열이 필요합니다.")
    if ((values < 0) | (values > 1)).any() or not 0 <= threshold <= 1:
        raise ValueError("확률과 threshold는 0~1 범위여야 합니다.")
    return (values >= threshold).astype(int)

if __name__ == "__main__":
    print(predict_labels([0.15, 0.50, 0.81], threshold=0.5))
