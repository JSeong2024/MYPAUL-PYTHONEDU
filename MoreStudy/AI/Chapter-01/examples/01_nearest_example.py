"""Example 01. 가장 가까운 학습 샘플을 이용해 Label을 예측합니다."""
import numpy as np


def closest_example(samples: np.ndarray, labels: np.ndarray, query: np.ndarray):
    if samples.ndim != 2 or query.shape != (samples.shape[1],):
        raise ValueError("입력 데이터의 차원이 일치해야 합니다.")
    distances = np.linalg.norm(samples - query, axis=1)
    index = int(np.argmin(distances))
    return str(labels[index]), float(distances[index]), index


def main() -> None:
    samples = np.array([[2, 1], [3, 2], [7, 7], [8, 6]], dtype=float)
    labels = np.array(["A", "A", "B", "B"])
    query = np.array([4, 3], dtype=float)
    predicted, distance, index = closest_example(samples, labels, query)
    print(f"가장 가까운 사례: {index + 1}번")
    print(f"거리: {distance:.3f}")
    print(f"분류 결과: {predicted}")
    print("이 방법은 참고 데이터를 비교하는 간단한 분류 방식입니다.")


if __name__ == "__main__":
    main()
