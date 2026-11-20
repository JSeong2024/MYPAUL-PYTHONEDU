"""Exercise 02 — 예측값의 변화가 손실에 미치는 영향 분석.

아래 예측값을 변경한 뒤 MSE, BCE, Cross-Entropy의 변화를 관찰하세요.
이 파일은 모델을 학습하지 않고 손실 함수의 계산만 비교합니다.
"""
import torch
from torch import nn

# 회귀: 정답은 80, 90점. 아래 예측값을 바꾸어 보세요.
actual_scores = torch.tensor([80.0, 90.0])
predicted_scores = torch.tensor([78.0, 91.0])  # 변경할 값
mse = nn.MSELoss()(predicted_scores, actual_scores)

# 이진 분류: 정답이 1. 예측 Logit을 양수와 음수로 변경해 보세요.
label_binary = torch.tensor([1.0])
logit_binary = torch.tensor([2.0])            # 변경할 값
binary_probability = torch.sigmoid(logit_binary)
bce = nn.BCEWithLogitsLoss()(logit_binary, label_binary)

# 다중 클래스: 클래스 0, 1, 2 중 정답은 2. 아래 점수의 순서를 바꿔 보세요.
label_class = torch.tensor([2])
logits = torch.tensor([[1.0, 2.0, 3.0]])     # 변경할 값
class_probabilities = torch.softmax(logits, dim=1)
ce = nn.CrossEntropyLoss()(logits, label_class)

print(f"MSE: {mse.item():.4f}")
print(f"Sigmoid 출력(정답=1): {binary_probability.item():.4f} / BCE: {bce.item():.4f}")
print("Softmax 출력:", [round(float(v), 4) for v in class_probabilities[0]])
print(f"Cross-Entropy: {ce.item():.4f}")
print("예측값의 변화에 따라 각 손실이 증가하거나 감소하는지 확인하세요.")
