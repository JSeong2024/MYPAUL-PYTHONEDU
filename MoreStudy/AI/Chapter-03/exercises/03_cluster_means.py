"""Practice 03: 각 Cluster의 중심을 산술평균으로 계산한다."""
import numpy as np


def update_centers(X, labels, n_clusters):
    """모든 Cluster가 1개 이상의 샘플을 갖는 입력을 가정한다."""
    raise NotImplementedError("update_centers()를 구현하세요.")

if __name__ == "__main__":
    X = np.array([[0., 0.], [2., 2.], [8., 8.], [10., 10.]])
    labels = np.array([0, 0, 1, 1])
    print(update_centers(X, labels, 2))
