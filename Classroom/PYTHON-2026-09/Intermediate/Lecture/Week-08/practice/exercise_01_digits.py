"""Exercise 01 — Epoch·은닉 노드 수를 검증(Validation) 정확도로 비교합니다.

전체 데이터의 60%로 학습, 20%로 후보를 비교합니다.
검증 결과로 최선의 설정을 선택한 뒤, Train+Validation(80%)로 다시 학습하고
나머지 20%의 Test 데이터로 최종 평가합니다.
"""
import random

import numpy as np
import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

SEED = 42
BATCH_SIZE = 64
LEARNING_RATE = 0.01

# 숫자 이미지: 픽셀 0~16 → 0~1로 정규화
raw = load_digits()
X = (raw.data / 16.0).astype(np.float32)
y = raw.target.astype(np.int64)

# 분리 기준: Train 60% / Validation 20% / Test 20%
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_dev, y_dev, test_size=0.25, random_state=SEED, stratify=y_dev
)


def train_model(X_learning, y_learning, epochs, hidden_units):
    """주어진 데이터만으로 모델을 학습하고 마지막 Train Loss와 함께 반환합니다."""
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.set_num_threads(min(2, torch.get_num_threads()))

    dataset = TensorDataset(torch.from_numpy(X_learning), torch.from_numpy(y_learning))
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    model = nn.Sequential(
        nn.Linear(64, hidden_units),
        nn.ReLU(),
        nn.Linear(hidden_units, 10),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_fn = nn.CrossEntropyLoss()
    last_loss = 0.0

    for _ in range(epochs):
        model.train()
        total_loss = 0.0
        for features, labels in loader:
            optimizer.zero_grad()
            logits = model(features)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(labels)
        last_loss = total_loss / len(X_learning)

    return model, last_loss


def evaluate_accuracy(model, X_eval, y_eval):
    model.eval()
    with torch.inference_mode():
        predictions = model(torch.from_numpy(X_eval)).argmax(dim=1).numpy()
    return float((predictions == y_eval).mean())


# (Epoch, 은닉 노드 수) — 학습 및 검증용 후보 비교
experiments = [(5, 64), (15, 64), (30, 64), (15, 16), (15, 128)]
results = []
print("Epoch | Hidden Units | Train Loss | Validation Accuracy")
for epochs, hidden_units in experiments:
    candidate, train_loss = train_model(X_train, y_train, epochs, hidden_units)
    val_accuracy = evaluate_accuracy(candidate, X_val, y_val)
    results.append((epochs, hidden_units, train_loss, val_accuracy))
    print(f"{epochs:>5} | {hidden_units:>12} | {train_loss:>10.4f} | {val_accuracy:>18.1%}")

# 동일 점수일 때는 목록에서 먼저 제시한 후보를 선택
best = max(results, key=lambda row: row[3])
print(f"\n검증 결과로 선택한 설정: EPOCHS={best[0]}, HIDDEN_UNITS={best[1]}")

# 모델 선택이 끝난 후에만 Test 데이터 사용
final_model, _ = train_model(X_dev, y_dev, best[0], best[1])
final_accuracy = evaluate_accuracy(final_model, X_test, y_test)
print(f"최종 Test Accuracy: {final_accuracy:.1%} ({len(y_test)}개 평가)")
print("Test 데이터는 후보 설정을 고르는 데 사용하지 않았습니다.")
