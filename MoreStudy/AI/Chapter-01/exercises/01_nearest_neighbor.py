"""Coding Practice 01 — 가장 가까운 참고 사례의 정답을 구합니다."""
import numpy as np


def predict_one(samples: np.ndarray, labels: np.ndarray, query: np.ndarray) -> str:
    # TODO: 모든 참고 사례와 query 사이의 유클리드 거리를 구합니다.
    # TODO: 가장 가까운 사례의 인덱스를 찾고 그 사례의 label을 반환합니다.
    raise NotImplementedError("TODO: predict_one")


if __name__ == "__main__":
    samples = np.array([[1, 2], [4, 5], [8, 9]], dtype=float)
    labels = np.array(["A", "B", "C"])
    query = np.array([5, 5], dtype=float)
    print(predict_one(samples, labels, query))  # 예상 결과: B
