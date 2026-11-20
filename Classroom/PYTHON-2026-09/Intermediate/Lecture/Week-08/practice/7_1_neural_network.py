"""7.1 — NumPy로 인공신경망 순전파 확인 (고정 가중치, 학습 없음)."""
import numpy as np

# 입력 특징 2개 (학습용 가상 입력)
x = np.array([0.6, 0.8])

# 입력층 2 → 은닉층 3 → 출력층 1
W1 = np.array([[0.4, -0.3, 0.7], [0.2, 0.6, -0.1]])
b1 = np.array([0.1, 0.0, 0.2])
W2 = np.array([[0.5], [-0.4], [0.8]])
b2 = np.array([0.1])

z = x @ W1 + b1
hidden = np.maximum(z, 0)  # ReLU: 음수는 0으로, 양수는 그대로
output = hidden @ W2 + b2

print("입력:", x)
print("은닉층 가중합:", np.round(z, 3))
print("은닉층 ReLU 출력:", np.round(hidden, 3))
print("최종 출력:", np.round(output, 3))
print("참고: 이 예제는 고정 가중치로 계산만 수행하며, 예측 모델을 학습하지 않습니다.")
