"""Exercise 01 — Epoch와 은닉 노드 수를 바꿔 결과를 비교하세요.

각 조건에서 같은 데이터 분할 및 난수 설정을 사용합니다.
조건 변경에 따른 성능 비교를 위한 실습이며, 테스트 데이터에서 얻은 성능을
최종 모델 선택에 반복 사용해서는 안 된다는 점은 Chapter 6.4를 참고하세요.
"""
import random
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

SEED = 42
BATCH_SIZE = 64
LR = 0.01

digits = load_digits()
X = (digits.data / 16.0).astype(np.float32)
y = digits.target.astype(np.int64)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)

def train_and_evaluate(epochs, hidden_units):
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    loader = DataLoader(TensorDataset(torch.from_numpy(X_train),
                                      torch.from_numpy(y_train)),
                        batch_size=BATCH_SIZE, shuffle=True)
    model = nn.Sequential(nn.Linear(64, hidden_units), nn.ReLU(),
                          nn.Linear(hidden_units, 10))
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.CrossEntropyLoss()
    last_loss = 0.0
    for _ in range(epochs):
        model.train()
        total = 0.0
        for features, targets in loader:
            optimizer.zero_grad()
            logits = model(features)
            loss = loss_fn(logits, targets)
            loss.backward()
            optimizer.step()
            total += loss.item() * len(targets)
        last_loss = total / len(X_train)
    model.eval()
    with torch.inference_mode():
        pred = model(torch.from_numpy(X_test)).argmax(dim=1).numpy()
    return last_loss, float((pred == y_test).mean())

# 아래 조건을 바꾸거나 추가하면서 비교해 보세요.
experiments = [
    (5, 64),
    (15, 64),
    (30, 64),
    (15, 16),
    (15, 128),
]

print("Epoch | Hidden Units | Train Loss | Test Accuracy")
for epochs, hidden_units in experiments:
    loss, accuracy = train_and_evaluate(epochs, hidden_units)
    print(f"{epochs:>5} | {hidden_units:>12} | {loss:>10.4f} | {accuracy:>12.1%}")
print("두 지표가 항상 같은 방향으로 변화하는지 정리해 보세요.")
