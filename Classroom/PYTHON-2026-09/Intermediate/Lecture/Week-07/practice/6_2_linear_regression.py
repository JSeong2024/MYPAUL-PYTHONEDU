"""6.2 | 공부 시간 → 점수 예측. 모델 불러오기·준비·분할·생성·학습·평가·예측."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# 1. 데이터 준비 — 각 행은 학생 한 명, 입력 특징은 공부 시간 한 개
X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
y = [42, 48, 53, 57, 62, 70, 74, 77, 84, 89]

# 2. 학습용 80% / 테스트용 20% 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"데이터: Train {len(X_train)}개 / Test {len(X_test)}개")

# 3. 모델 생성: 아직 학습하지 않은 LinearRegression 객체
model = LinearRegression()

# 4. 학습: 학습용 입력과 정답만 전달
model.fit(X_train, y_train)

# 5. 테스트 데이터 예측 및 평가
pred_test = model.predict(X_test)
print("\n[테스트 데이터: 실제 점수 vs 예측 점수]")
for hours, actual, predicted in zip(X_test, y_test, pred_test):
    print(f"{hours[0]}시간: 실제 {actual}점 / 예측 {predicted:.1f}점")
print(f"MAE: {mean_absolute_error(y_test, pred_test):.2f}점")

# 6. 새로운 입력으로 예측 — 이 값의 정답은 알려져 있지 않음
hours = 6.5
prediction = model.predict([[hours]])[0]
print(f"\n새로운 입력 {hours}시간의 예상 점수: {prediction:.1f}점")
print(f"학습된 기울기: {model.coef_[0]:.3f}, 절편: {model.intercept_:.3f}")

# 시각화: 실제 데이터와 모델의 예측 직선
x_plot = np.linspace(1, 10, 100).reshape(-1, 1)
fig, ax = plt.subplots(figsize=(9.6, 5.6), dpi=160)
ax.scatter(np.asarray(X_train).ravel(), y_train, s=78, label="Train (8)", zorder=3)
ax.scatter(np.asarray(X_test).ravel(), y_test, s=94, marker="s", label="Test (2)", zorder=4)
ax.plot(x_plot.ravel(), model.predict(x_plot), linewidth=2.5, label="Linear Regression")
ax.scatter([hours], [prediction], s=150, marker="*", label="New input: 6.5 h", zorder=5)
ax.set(xlabel="Study hours (h)", ylabel="Exam score (points)", title="6.2  |  Linear Regression: Train / Test / New Input")
ax.legend(loc="upper left")
ax.grid(alpha=0.2)
fig.tight_layout()
output = Path("assets")
output.mkdir(exist_ok=True)
fig.savefig(output / "6_2_linear_regression.png", bbox_inches="tight", facecolor="white")
plt.show()
