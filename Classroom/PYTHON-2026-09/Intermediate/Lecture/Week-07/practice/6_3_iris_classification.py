"""6.3 | 붓꽃 품종 분류: 2개 특징, KNN, 학습/테스트, 결정 영역."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data[:, :2]  # 꽃받침 길이, 꽃받침 너비(cm)
y = iris.target       # 품종을 나타내는 0, 1, 2

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("입력 특징:", iris.feature_names[:2])
print("분류할 품종:", list(iris.target_names))
print(f"학습 {len(X_train)}개 / 테스트 {len(X_test)}개")
print(f"테스트 정확도: {accuracy:.3f} ({sum(predictions == y_test)}/{len(y_test)})")

new_flower = [[5.7, 2.8]]  # 새로운 꽃의 꽃받침 길이/너비 (cm)
predicted_class = model.predict(new_flower)[0]
print("새 꽃 [5.7, 2.8] →", iris.target_names[predicted_class])

# 서로 다른 입력값에서 모델이 어떤 품종을 선택하는지 배경색으로 표시
x_min, x_max = X[:, 0].min() - 0.35, X[:, 0].max() + 0.35
y_min, y_max = X[:, 1].min() - 0.3, X[:, 1].max() + 0.3
xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 350),
    np.linspace(y_min, y_max, 300),
)
mesh = np.c_[xx.ravel(), yy.ravel()]
regions = model.predict(mesh).reshape(xx.shape)

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"][:3]
fig, ax = plt.subplots(figsize=(9.6, 6.1))
ax.contourf(xx, yy, regions, alpha=0.14,
            cmap=ListedColormap(colors), levels=[-0.5, 0.5, 1.5, 2.5])
for class_idx, class_name in enumerate(iris.target_names):
    train_mask = y_train == class_idx
    ax.scatter(X_train[train_mask, 0], X_train[train_mask, 1],
               s=48, color=colors[class_idx], label=class_name,
               edgecolors="white", linewidths=0.5, alpha=0.92)
# 검정 테두리가 있는 큰 원은 모델 학습에 사용하지 않은 데이터
ax.scatter(X_test[:, 0], X_test[:, 1], s=112,
           facecolors="none", edgecolors="black", linewidths=1.25,
           label="Test Sample", zorder=5)
ax.set(xlabel="Sepal Length (cm)", ylabel="Sepal Width (cm)",
       title="KNN Classification: Iris (2 Features)")
ax.legend(loc="upper right", framealpha=0.94)
ax.grid(alpha=0.16)
fig.tight_layout()
out = Path(__file__).resolve().parent.parent / "assets" / "6_3_iris_knn.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=180, facecolor="white", bbox_inches="tight")
print(f"그래프 저장: {out}")
if "agg" not in plt.get_backend().lower():
    plt.show()
