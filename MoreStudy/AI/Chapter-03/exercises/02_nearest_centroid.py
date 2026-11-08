"""Practice 02: 각 샘플을 가장 가까운 중심에 할당한다."""
import numpy as np


def assign_clusters(X, centers):
    """X: (n, d), centers: (k, d). 각 행에 대해 0..k-1 ID를 반환한다."""
    raise NotImplementedError("assign_clusters()를 구현하세요.")

if __name__ == "__main__":
    X = np.array([[0., 1.], [9., 9.], [2., 2.]])
    centers = np.array([[0., 0.], [10., 10.]])
    print(assign_clusters(X, centers))
