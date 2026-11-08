"""Coding Practice 03 — 지정한 기준보다 낮은 예측을 사람 검토로 보냅니다."""
import numpy as np


def review_flags(votes: np.ndarray, threshold: float) -> np.ndarray:
    # TODO: votes < threshold인 위치에 True를 반환합니다.
    raise NotImplementedError("TODO: review_flags")


if __name__ == "__main__":
    votes = np.array([1.0, 0.8, 0.6, 0.4])
    print(review_flags(votes, 0.8))  # 예상 결과: [False False  True  True]
