"""7.2 — PyTorch로 scikit-learn Digits(8×8) 분류 학습.

별도 데이터 파일 불필요. CPU 실행 가능. 실행 후 이미지 두 개를 assets/에 저장합니다.
"""
from pathlib import Path
import random

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

SEED = 42
EPOCHS = 15            # 학습 반복 횟수: 5, 15, 30으로 바꾸어 보세요.
HIDDEN_UNITS = 64       # 은닉층 노드: 16, 64, 128을 비교해 보세요.
BATCH_SIZE = 64
LEARNING_RATE = 0.01

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.set_num_threads(min(2, torch.get_num_threads()))

# Notebook에서는 assets/, Python 파일 실행 시에는 Week-08/assets/ 사용
out_dir = (Path(__file__).resolve().parents[1] / "assets") if "__file__" in globals() else Path("assets")
out_dir.mkdir(parents=True, exist_ok=True)

digits = load_digits()
X = (digits.data / 16.0).astype(np.float32)  # 8x8 → 특징 64개, 픽셀값 0~1
y = digits.target.astype(np.int64)          # 정답: 0~9
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)

train_loader = DataLoader(
    TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train)),
    batch_size=BATCH_SIZE, shuffle=True
)

# nn.Linear(입력 특징 수, 출력 뉴런 수): 64픽셀 → 은닉층 → 10개 숫자 점수
# nn.Sequential은 Linear → ReLU → Linear 순서대로 층을 연결합니다.
model = nn.Sequential(
    nn.Linear(64, HIDDEN_UNITS),
    nn.ReLU(),
    nn.Linear(HIDDEN_UNITS, 10),
)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

loss_history = []
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0
    for features, labels in train_loader:
        optimizer.zero_grad()
        logits = model(features)
        loss = loss_fn(logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
    train_loss = total_loss / len(X_train)
    loss_history.append(train_loss)
    print(f"Epoch {epoch+1:02d}/{EPOCHS} | Train Loss: {train_loss:.4f}")

# 평가 시에는 학습용 동작을 멈추고, 기울기 계산도 별도로 생략합니다.
model.eval()
with torch.inference_mode():
    predictions = model(torch.from_numpy(X_test)).argmax(dim=1).numpy()
accuracy = float(np.mean(predictions == y_test))
print(f"Test Accuracy: {accuracy:.1%} ({np.sum(predictions == y_test)}/{len(y_test)})")

# Figure 1 — 학습 손실 곡선
fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=170)
ax.plot(range(1, EPOCHS+1), loss_history, marker="o", linewidth=2.4, markersize=5)
ax.set_title("Training Loss by Epoch", fontsize=16, pad=16)
ax.set_xlabel("Epoch")
ax.set_ylabel("Train Loss")
ax.set_xticks(range(1, EPOCHS+1))
ax.grid(alpha=0.22)
fig.tight_layout()
fig.savefig(out_dir / "7_2_training_curve.png", facecolor="white", dpi=170)
plt.show()

# Figure 2 — 테스트 이미지와 예측 숫자 비교
fig, axes = plt.subplots(3, 4, figsize=(10, 8.1), dpi=170)
for i, ax in enumerate(axes.flat):
    ax.imshow(X_test[i].reshape(8, 8), cmap="gray_r", interpolation="nearest")
    correct = predictions[i] == y_test[i]
    ax.set_title(f"True {y_test[i]}  /  Pred {predictions[i]}" + ("" if correct else "  *"), fontsize=10)
    ax.axis("off")
fig.suptitle("Handwritten Digit Classification — Test Samples", fontsize=15)
fig.tight_layout(pad=1.9, h_pad=2.2)
fig.savefig(out_dir / "7_2_digits_predictions.png", facecolor="white", dpi=170)
plt.show()
