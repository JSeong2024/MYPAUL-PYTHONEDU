"""6.4 | Train/Validation/Test로 특징 비교 → 선택 후 Test 한 번 평가."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# 1. 정답과 전체 특징을 읽음. 아직 특징 선택에 테스트 결과를 사용하지 않음.
iris = load_iris()
X = iris.data  # 꽃받침 길이·너비 / 꽃잎 길이·너비 (4개)
y = iris.target

# 2. 전체의 20%를 마지막 테스트용으로 보관
X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# 3. 남은 80%를 Train 75% / Validation 25%로 나눔
#    전체 기준 60% / 20% / 20%
X_train, X_val, y_train, y_val = train_test_split(
    X_dev, y_dev, test_size=0.25, random_state=42, stratify=y_dev
)
print(f"Train: {len(X_train)} / Validation: {len(X_val)} / Test: {len(X_test)}")

# 4. 모델은 고정하고, 입력 Feature만 변경해 검증 성능을 비교
feature_sets = {
    "Sepal": [0, 1],
    "Petal": [2, 3],
}
validation_scores = {}
for name, cols in feature_sets.items():
    candidate = KNeighborsClassifier(n_neighbors=5)
    candidate.fit(X_train[:, cols], y_train)
    val_predictions = candidate.predict(X_val[:, cols])
    validation_scores[name] = accuracy_score(y_val, val_predictions)
    print(f"{name} Validation Accuracy: {validation_scores[name]:.3f}")

# 5. 검증 정확도가 높은 특징 선택. Test 데이터는 선택에 사용하지 않음.
best_name = max(validation_scores, key=validation_scores.get)
best_cols = feature_sets[best_name]
print("Selected features:", best_name)

# 6. 선택을 마친 뒤 개발용 전체(Train+Validation)로 최종 모델 학습
final_model = KNeighborsClassifier(n_neighbors=5)
final_model.fit(X_dev[:, best_cols], y_dev)

# 7. 보관했던 Test로 최종 평가
final_predictions = final_model.predict(X_test[:, best_cols])
final_acc = accuracy_score(y_test, final_predictions)
cm = confusion_matrix(y_test, final_predictions)
print(f"Final Test Accuracy: {final_acc:.3f} ({(final_predictions == y_test).sum()}/{len(y_test)})")
print("Confusion matrix (rows=actual, columns=predicted):\n", cm)

out = Path("assets")
out.mkdir(exist_ok=True)
fig, ax = plt.subplots(figsize=(7.9, 4.9), dpi=170)
labels = list(validation_scores)
values = [validation_scores[l] * 100 for l in labels]
bars = ax.bar(labels, values, width=0.48)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, v + 1.1, f"{v:.1f}%", ha="center", fontsize=12)
ax.set_ylim(0, 108)
ax.set_ylabel("Validation accuracy (%)")
ax.set_title("6.4  |  Feature Selection with Validation Set")
ax.grid(axis="y", alpha=0.17)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(out / "6_4_feature_comparison.png", bbox_inches="tight", facecolor="white")
plt.show()

fig, ax = plt.subplots(figsize=(7.1, 5.7), dpi=170)
ConfusionMatrixDisplay(cm, display_labels=iris.target_names).plot(ax=ax, values_format="d", cmap="Blues", colorbar=False)
ax.set_title(f"6.4  |  Final Test: {final_acc:.1%} accuracy")
fig.tight_layout()
fig.savefig(out / "6_4_confusion_matrix.png", bbox_inches="tight", facecolor="white")
plt.show()
