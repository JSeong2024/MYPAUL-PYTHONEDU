"""Coding Practice 01 — 정답 구현."""
import numpy as np


def predict_one(samples: np.ndarray, labels: np.ndarray, query: np.ndarray) -> str:
    if len(samples) == 0 or len(samples) != len(labels):
        raise ValueError("참고 사례와 레이블이 같은 개수로 존재해야 합니다.")
    distances = np.linalg.norm(samples - query, axis=1)
    return str(labels[int(np.argmin(distances))])


if __name__ == "__main__":
    print(predict_one(
        np.array([[1, 2], [4, 5], [8, 9]], dtype=float),
        np.array(["A", "B", "C"]), np.array([5, 5], dtype=float),
    ))
