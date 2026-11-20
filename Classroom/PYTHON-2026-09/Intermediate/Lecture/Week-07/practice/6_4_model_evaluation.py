"""6.4 | Train/Validation/Test: 특징 선택, 최종 평가, 혼동행렬 시각화."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
y = iris.target
indices = np.arange(len(y))

# 20%는 최종 테스트용으로 보관. 모델 선택에 사용하지 않음.
train_val_idx, test_idx = train_test_split(
    indices, test_size=0.2, random_state=42, stratify=y
)
# 남은 80%에서 25%를 검증용으로 분리: 전체 기준 60/20/20
train_idx, val_idx = train_test_split(
    train_val_idx, test_size=0.25, random_state=42,
    stratify=y[train_val_idx]
)

feature_sets = {
    "Sepal (2 features)": [0, 1],
    "Petal (2 features)": [2, 3],
}
validation_scores = {}
for title, feature_columns in feature_sets.items():
    X = iris.data[:, feature_columns]
    candidate = KNeighborsClassifier(n_neighbors=5)
    candidate.fit(X[train_idx], y[train_idx])
    val_pred = candidate.predict(X[val_idx])
    validation_scores[title] = accuracy_score(y[val_idx], val_pred)

best_title = max(validation_scores, key=validation_scores.get)
best_features = feature_sets[best_title]
X_best = iris.data[:, best_features]

# 검증으로 특징을 선택한 뒤 전체 학습용 80%로 다시 학습
final_model = KNeighborsClassifier(n_neighbors=5)
final_model.fit(X_best[train_val_idx], y[train_val_idx])
final_pred = final_model.predict(X_best[test_idx])
final_accuracy = accuracy_score(y[test_idx], final_pred)
cm = confusion_matrix(y[test_idx], final_pred, labels=[0, 1, 2])

print(f"학습 {len(train_idx)} / 검증 {len(val_idx)} / 테스트 {len(test_idx)}")
for title, score in validation_scores.items():
    print(f"검증 정확도 - {title}: {score:.3f}")
print("선택한 특징:", best_title)
print(f"최종 테스트 정확도: {final_accuracy:.3f} ({sum(final_pred == y[test_idx])}/{len(test_idx)})")
print("혼동행렬 (행=실제, 열=예측):")
print(cm)

out_dir = Path(__file__).resolve().parent.parent / "assets"
out_dir.mkdir(parents=True, exist_ok=True)

# 비교 그래프: 검증 데이터 기준, 테스트 데이터로 후보 선택하지 않음
fig, ax = plt.subplots(figsize=(8.4, 5.4))
labels = list(validation_scores)
values = list(validation_scores.values())
bars = ax.bar(labels, values, width=0.48)
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 0.018,
            f"{value:.1%}", ha="center", fontsize=12, fontweight="bold")
ax.set(ylim=(0, 1.14), ylabel="Validation Accuracy",
       title="Feature Selection: Validation Accuracy")
ax.grid(axis="y", alpha=0.18)
ax.set_axisbelow(True)
fig.tight_layout()
bar_path = out_dir / "6_4_feature_comparison.png"
fig.savefig(bar_path, dpi=180, facecolor="white", bbox_inches="tight")
print(f"그래프 저장: {bar_path}")
if "agg" not in plt.get_backend().lower():
    plt.show()

# 최종 테스트 혼동행렬
fig, ax = plt.subplots(figsize=(7.8, 6.4))
display = ConfusionMatrixDisplay(
    confusion_matrix=cm, display_labels=iris.target_names
)
display.plot(ax=ax, cmap="Blues", colorbar=False, values_format="d")
ax.set_title("Final Test: Confusion Matrix")
fig.tight_layout()
cm_path = out_dir / "6_4_confusion_matrix.png"
fig.savefig(cm_path, dpi=180, facecolor="white", bbox_inches="tight")
print(f"그래프 저장: {cm_path}")
if "agg" not in plt.get_backend().lower():
    plt.show()
