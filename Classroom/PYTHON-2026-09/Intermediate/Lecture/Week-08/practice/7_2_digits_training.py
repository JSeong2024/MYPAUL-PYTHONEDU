"""7.2: PyTorch로 8×8 손글씨 숫자(0~9) 분류 신경망 학습.

별도 CSV 불필요. CPU 실행 가능. 실행하면 학습 곡선과 예측 이미지가 assets/에 저장됨.
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
EPOCHS = 15
LEARNING_RATE = 0.01
BATCH_SIZE = 64
HIDDEN_UNITS = 64

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.set_num_threads(min(torch.get_num_threads(), 2))

out_dir = (Path(__file__).resolve().parents[1] / "assets") if "__file__" in globals() else Path("assets")
out_dir.mkdir(parents=True, exist_ok=True)

digits = load_digits()
X = (digits.data / 16.0).astype(np.float32)   # 8×8 픽셀 64개, 값 0~1
y = digits.target.astype(np.int64)            # 실제 숫자 0~9

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)
train_loader = DataLoader(
    TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train)),
    batch_size=BATCH_SIZE, shuffle=True,
)

# 입력 64개(8×8) → 은닉층 64개 → 출력 10개(숫자 0~9)
model = nn.Sequential(
    nn.Linear(64, HIDDEN_UNITS),
    nn.ReLU(),
    nn.Linear(HIDDEN_UNITS, 10),
)
criterion = nn.CrossEntropyLoss()  # 숫자 종류를 구분하는 분류 손실함수
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

loss_history = []
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        logits = model(inputs)
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(targets)
    avg_loss = total_loss / len(X_train)
    loss_history.append(avg_loss)
    print(f"Epoch {epoch + 1:02d}/{EPOCHS} | Train Loss: {avg_loss:.4f}")

# 학습 완료 후 테스트 데이터에 대한 예측
model.eval()
with torch.no_grad():
    test_logits = model(torch.from_numpy(X_test))
    predictions = test_logits.argmax(dim=1).numpy()
accuracy = (predictions == y_test).mean()
print(f"Test Accuracy: {accuracy:.1%} ({(predictions == y_test).sum()}/{len(y_test)})")

# 시각화 1 — 학습이 진행되는 동안 Loss 변화
plt.figure(figsize=(9, 5.3), dpi=160)
plt.plot(range(1, EPOCHS + 1), loss_history, marker="o", linewidth=2)
plt.title("Training Loss by Epoch")
plt.xlabel("Epoch")
plt.ylabel("Training Loss")
plt.xticks(range(1, EPOCHS + 1))
plt.grid(alpha=0.28)
plt.tight_layout()
plt.savefig(out_dir / "7_2_training_curve.png", facecolor="white", dpi=160)
plt.show()

# 시각화 2 — 처음 12개 테스트 이미지의 예측 결과
fig, axes = plt.subplots(3, 4, figsize=(10, 8), dpi=160)
for i, ax in enumerate(axes.flat):
    ax.imshow(X_test[i].reshape(8, 8), cmap="gray_r", interpolation="nearest")
    correct = predictions[i] == y_test[i]
    ax.set_title(f"True: {y_test[i]} / Pred: {predictions[i]}" + ("" if correct else " *"), fontsize=9)
    ax.axis("off")
fig.suptitle("Handwritten Digit Classification: Test Samples", fontsize=14)
fig.tight_layout(pad=2.2, h_pad=2.4, w_pad=1.0)
fig.savefig(out_dir / "7_2_digits_predictions.png", facecolor="white", dpi=160)
plt.show()
