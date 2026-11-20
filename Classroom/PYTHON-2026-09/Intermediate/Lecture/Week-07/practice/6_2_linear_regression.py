"""6.2 | 공부 시간과 점수: 선형 회귀 학습/테스트 분리/그래프 생성."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
y = [42, 48, 53, 57, 62, 70, 74, 77, 84, 89]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

hours = 6.5
predicted_score = model.predict([[hours]])[0]
print(f"학습 데이터: {len(X_train)}개 / 테스트 데이터: {len(X_test)}개")
print(f"X_train: {X_train}")
print(f"y_train: {y_train}")
print(f"X_test: {X_test}")
print(f"y_test: {y_test}")
print(f"학습된 기울기(a): {model.coef_[0]:.3f}")
print(f"학습된 절편(b): {model.intercept_:.3f}")
print(f"공부 시간 {hours}시간 → 예상 점수 {predicted_score:.1f}점")

hours_range = np.linspace(1, 10, 100).reshape(-1, 1)
predicted_scores = model.predict(hours_range)

fig, ax = plt.subplots(figsize=(9.6, 5.9))
ax.scatter([row[0] for row in X_train], y_train,
           label="Training Data", s=72, zorder=3)
ax.scatter([row[0] for row in X_test], y_test,
           label="Test Data", s=85, marker="s", zorder=4)
ax.plot(hours_range, predicted_scores,
        label="Prediction", color="firebrick", linewidth=2.4)
ax.set(title="Linear Regression: Study Hours and Exam Score",
       xlabel="Study Hours", ylabel="Exam Score")
ax.set_xlim(0.5, 10.5)
ax.set_ylim(35, 95)
ax.legend(loc="upper left")
ax.grid(alpha=0.22)
fig.tight_layout()
out = Path(__file__).resolve().parent.parent / "assets" / "6_2_linear_regression.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=180, facecolor="white", bbox_inches="tight")
print(f"그래프 저장: {out}")
if "agg" not in plt.get_backend().lower():
    plt.show()
