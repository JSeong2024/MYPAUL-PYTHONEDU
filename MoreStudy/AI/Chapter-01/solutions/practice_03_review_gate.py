"""Coding Practice 03 — 정답 구현."""
import numpy as np


def review_flags(votes: np.ndarray, threshold: float) -> np.ndarray:
    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("기준은 0~1 사이여야 합니다.")
    votes = np.asarray(votes, dtype=float)
    if not np.isfinite(votes).all() or np.any((votes < 0) | (votes > 1)):
        raise ValueError("투표 비율은 0~1 사이여야 합니다.")
    return votes < threshold


if __name__ == "__main__":
    print(review_flags(np.array([1, 0.8, 0.6, 0.4]), 0.8))
