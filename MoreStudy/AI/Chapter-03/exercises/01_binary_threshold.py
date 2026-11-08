"""Practice 01: Class 1의 예측 확률로 Label을 결정한다."""
import numpy as np


def predict_labels(probabilities, threshold=0.5):
    """각 확률이 threshold 이상이면 1, 아니면 0을 반환한다."""
    raise NotImplementedError("predict_labels()를 구현하세요.")

if __name__ == "__main__":
    print(predict_labels(np.array([0.15, 0.50, 0.81]), threshold=0.5))
