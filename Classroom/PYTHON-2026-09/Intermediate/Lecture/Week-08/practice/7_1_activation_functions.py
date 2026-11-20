"""7.1 — Sigmoid, ReLU, Softmax, GELU의 출력과 그래프 비교.

Google Colab 또는 CPU Python에서 실행할 수 있습니다.
필요 라이브러리: numpy, torch, matplotlib
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn import functional as F

# 노트북에서는 현재 폴더, Python 파일에서는 Week-08 폴더에 이미지 저장
OUT_DIR = (
    Path(__file__).resolve().parents[1] / "assets"
    if "__file__" in globals()
    else Path("assets")
)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 단일 입력에 적용하는 활성화 함수 비교
samples = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
print("입력값: ", samples.tolist())
for name, result in (
    ("Sigmoid", torch.sigmoid(samples)),
    ("ReLU", F.relu(samples)),
    ("GELU", F.gelu(samples)),
):
    print(f"{name:>8}: ", [round(float(v), 4) for v in result])

# 2. 곡선 시각화
x = torch.linspace(-4, 4, 400)
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=175)
ax.plot(x.numpy(), torch.sigmoid(x).numpy(), label="Sigmoid", linewidth=2.5)
ax.plot(x.numpy(), F.relu(x).numpy(), label="ReLU", linewidth=2.5)
ax.plot(x.numpy(), F.gelu(x).numpy(), label="GELU", linewidth=2.5)
ax.axhline(0, linewidth=0.7, alpha=0.4, color="gray")
ax.axvline(0, linewidth=0.7, alpha=0.4, color="gray")
ax.set_title("Activation Functions: Sigmoid, ReLU, GELU", fontsize=16, pad=14)
ax.set_xlabel("Input (x)")
ax.set_ylabel("Output")
ax.set_xlim(-4, 4)
ax.set_ylim(-0.6, 4.25)
ax.grid(alpha=0.23)
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(OUT_DIR / "7_1_activation_curves.png", dpi=175, facecolor="white")
plt.show()
plt.close(fig)

# 3. Softmax는 여러 클래스의 점수를 함께 변환함
logits = torch.tensor([1.0, 2.0, 3.0])  # A, B, C에 대한 원시 점수
probs = F.softmax(logits, dim=0)
print("Softmax 입력(원시 점수):", logits.tolist())
print("Softmax 출력(분포):", [round(float(v), 4) for v in probs])
print("출력값의 합:", round(float(probs.sum()), 4))

labels = ["Class A", "Class B", "Class C"]
fig, ax = plt.subplots(figsize=(8.6, 5.2), dpi=175)
bars = ax.bar(labels, (probs * 100).numpy(), width=0.55)
for bar, p in zip(bars, probs):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5, f"{float(p):.1%}",
            ha="center", fontsize=12)
ax.set_ylim(0, 80)
ax.set_ylabel("Softmax Output (%)")
ax.set_title("Softmax: Scores [1, 2, 3] → Class Distribution", fontsize=15, pad=14)
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(OUT_DIR / "7_1_softmax_example.png", dpi=175, facecolor="white")
plt.show()
plt.close(fig)
