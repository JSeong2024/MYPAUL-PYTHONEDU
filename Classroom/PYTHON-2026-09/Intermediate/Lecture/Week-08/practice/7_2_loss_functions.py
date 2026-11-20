"""7.2 — MSE, BCEWithLogitsLoss, CrossEntropyLoss 비교.

간단한 가상 데이터를 사용하여 올바른 예측과 잘못된 예측의 손실을 계산합니다.
CPU에서 실행 가능하며, assets/7_2_loss_comparison.png를 생성합니다.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import torch
from torch import nn

OUT_DIR = (Path(__file__).resolve().parents[1] / "assets") if "__file__" in globals() else Path("assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. 회귀: 정답과 예측값 간 제곱 오차의 평균
mse_fn = nn.MSELoss()
actual_scores = torch.tensor([80.0, 90.0])
good_scores = torch.tensor([78.0, 91.0])
bad_scores = torch.tensor([65.0, 98.0])
mse_good = mse_fn(good_scores, actual_scores).item()
mse_bad = mse_fn(bad_scores, actual_scores).item()

# 2. 이진 분류: 정답이 1일 때, Sigmoid 전 원시 점수(Logit)로 손실 계산
bce_fn = nn.BCEWithLogitsLoss()
correct_binary = torch.tensor([1.0])     # 실수형 0 또는 1
logit_good = torch.tensor([2.0])         # Sigmoid 결과 약 0.881
logit_bad = torch.tensor([-2.0])         # Sigmoid 결과 약 0.119
bce_good = bce_fn(logit_good, correct_binary).item()
bce_bad = bce_fn(logit_bad, correct_binary).item()

# 3. 다중 클래스 분류: 클래스 0, 1, 2 중 정답이 2
ce_fn = nn.CrossEntropyLoss()
correct_class = torch.tensor([2])        # 정답 클래스 인덱스(정수)
logits_good = torch.tensor([[1.0, 2.0, 3.0]])
logits_bad = torch.tensor([[3.0, 2.0, 1.0]])
ce_good = ce_fn(logits_good, correct_class).item()
ce_bad = ce_fn(logits_bad, correct_class).item()

print(f"MSE  | 좋은 예측: {mse_good:.3f} | 나쁜 예측: {mse_bad:.3f}")
print(f"BCE  | 좋은 예측: {bce_good:.3f} | 나쁜 예측: {bce_bad:.3f}")
print(f"CE   | 좋은 예측: {ce_good:.3f} | 나쁜 예측: {ce_bad:.3f}")
print("BCE 확률 비교:", round(torch.sigmoid(logit_good).item(), 3),
      round(torch.sigmoid(logit_bad).item(), 3))
print("CE 정답 클래스 확률:",
      round(torch.softmax(logits_good, dim=1)[0, 2].item(), 3),
      round(torch.softmax(logits_bad, dim=1)[0, 2].item(), 3))

# 각 손실의 수치 범위가 다르므로 개별 y축으로 그립니다.
metrics = [
    ("MSE · Regression", mse_good, mse_bad),
    ("BCE · Binary Classification", bce_good, bce_bad),
    ("CE · Multiclass Classification", ce_good, ce_bad),
]
fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.3), dpi=180)
for ax, (title, good, bad) in zip(axes, metrics):
    bars = ax.bar(["Good", "Incorrect"], [good, bad], width=0.52,
                  color=["#508CA2", "#CB8F65"])
    ax.set_title(title, fontsize=11, pad=14)
    ax.set_ylabel("Loss (lower is better)")
    ax.set_ylim(0, max(good, bad)*1.24)
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    for b, val in zip(bars, [good, bad]):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+max(good, bad)*0.05,
                f"{val:.3f}", fontsize=11, ha="center")
fig.suptitle("Loss Functions — Correct vs. Incorrect Predictions", fontsize=15, y=1.05)
fig.text(0.5, -0.02, "Different loss scales: do not compare heights across tasks.",
         fontsize=10, color="#666666", ha="center")
fig.tight_layout()
fig.savefig(OUT_DIR / "7_2_loss_comparison.png", dpi=180, facecolor="white", bbox_inches="tight")
plt.show()
plt.close(fig)
