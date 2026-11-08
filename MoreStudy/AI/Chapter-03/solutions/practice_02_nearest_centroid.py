"""Practice 02 모범 구현."""
import numpy as np


def assign_clusters(X, centers):
    x = np.asarray(X, dtype=float)
    c = np.asarray(centers, dtype=float)
    if x.ndim != 2 or c.ndim != 2 or x.shape[1] != c.shape[1]:
        raise ValueError("X와 centers는 Feature 수가 같은 2차원 배열이어야 합니다.")
    if not len(c) or not np.isfinite(x).all() or not np.isfinite(c).all():
        raise ValueError("중심은 비어 있을 수 없고 모든 좌표는 유한해야 합니다.")
    distances = np.linalg.norm(x[:, None, :] - c[None, :, :], axis=2)
    return np.argmin(distances, axis=1)

if __name__ == "__main__":
    print(assign_clusters([[0, 1], [9, 9], [2, 2]], [[0, 0], [10, 10]]))
