"""Practice 03 모범 구현."""
import numpy as np


def update_centers(X, labels, n_clusters):
    x = np.asarray(X, dtype=float)
    y = np.asarray(labels, dtype=int)
    if x.ndim != 2 or y.ndim != 1 or len(x) != len(y) or n_clusters < 1:
        raise ValueError("X, labels, n_clusters의 형태가 맞지 않습니다.")
    if not np.isfinite(x).all() or (y < 0).any() or (y >= n_clusters).any():
        raise ValueError("좌표 또는 Cluster ID가 유효하지 않습니다.")
    if any(not np.any(y == i) for i in range(n_clusters)):
        raise ValueError("비어 있는 Cluster의 중심은 계산할 수 없습니다.")
    return np.vstack([x[y == i].mean(axis=0) for i in range(n_clusters)])

if __name__ == "__main__":
    print(update_centers([[0, 0], [2, 2], [8, 8], [10, 10]], [0, 0, 1, 1], 2))
