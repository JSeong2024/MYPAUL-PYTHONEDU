"""7.1: 작은 인공신경망의 순전파 계산 — NumPy만 사용."""
import numpy as np

# 두 개의 특징: [공부 시간(정규화), 수면 시간(정규화)]
x = np.array([0.6, 0.8])

# 입력 2개 → 은닉 노드 3개 → 출력 1개
W1 = np.array([[0.4, -0.3, 0.7], [0.2, 0.6, -0.1]])
b1 = np.array([0.1, 0.0, 0.2])
W2 = np.array([[0.5], [-0.4], [0.8]])
b2 = np.array([0.1])

hidden = np.maximum(x @ W1 + b1, 0)  # ReLU: 음수를 0으로
output = hidden @ W2 + b2

print("입력층:", x, "shape:", x.shape)
print("은닉층:", np.round(hidden, 3), "shape:", hidden.shape)
print("출력층:", np.round(output, 3), "shape:", output.shape)
print("주의: 학습하지 않은 임의의 가중치이므로 실제 시험 점수 예측이 아님")
