"""KMeans의 할당·중심 갱신을 NumPy로 한 번 구현한다."""
import numpy as np

X = np.array([[1., 1.], [1., 2.], [2., 1.], [7., 7.], [8., 7.], [7., 8.]])
centers = np.array([[1., 1.], [8., 8.]])
distances = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
labels = np.argmin(distances, axis=1)
updated = np.vstack([X[labels == group].mean(axis=0) for group in range(2)])
print("Assigned clusters:", labels.tolist())
print("Updated centers:\n", updated)
