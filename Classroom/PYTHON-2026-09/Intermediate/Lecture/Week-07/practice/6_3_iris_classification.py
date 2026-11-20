"""6.3 | KNN 붓꽃 분류. 길이·너비 특징, Train/Test, 새 꽃 예측, 결정 영역."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# 1. 데이터 준비: 꽃받침 길이·너비(cm)만 사용
iris = load_iris()
X = iris.data[:, :2]
y = iris.target

# 2. 데이터 분리: 품종 비율 유지
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. 모델 생성 (가까운 꽃 다섯 개 참조)
model = KNeighborsClassifier(n_neighbors=5)

# 4. 학습 (KNN은 학습 사례를 저장하고 거리를 예측 시점에 활용)
model.fit(X_train, y_train)

# 5. 테스트 데이터 예측 및 정확도 평가
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Train {len(X_train)}개 / Test {len(X_test)}개")
print(f"Test Accuracy: {accuracy:.3f} ({(predictions == y_test).sum()}/{len(y_test)})")

# 6. 새로운 꽃 예측
new_flower = [[5.7, 2.8]]  # 꽃받침 길이, 너비
species = iris.target_names[model.predict(new_flower)[0]]
print(f"꽃받침 {new_flower[0]} cm → {species}")

# 시각화: 모델이 구분하는 2차원 결정 영역
x_min, x_max = X[:, 0].min() - 0.35, X[:, 0].max() + 0.35
y_min, y_max = X[:, 1].min() - 0.35, X[:, 1].max() + 0.35
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 230), np.linspace(y_min, y_max, 180))
region = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
fig, ax = plt.subplots(figsize=(9.4, 5.8), dpi=160)
ax.contourf(xx, yy, region, levels=[-0.5, 0.5, 1.5, 2.5], cmap=ListedColormap(["#d7e9f5", "#e8dff8", "#f8e7cb"]), alpha=0.9)
for i, name in enumerate(iris.target_names):
    mask = y_train == i
    ax.scatter(X_train[mask, 0], X_train[mask, 1], s=35, label=f"Train: {name}")
ax.scatter(X_test[:, 0], X_test[:, 1], facecolors="none", edgecolors="black", linewidths=1.2, s=75, label="Test (outlined)")
ax.scatter(new_flower[0][0], new_flower[0][1], marker="*", s=185, c="black", label="New flower")
ax.set(xlabel="Sepal length (cm)", ylabel="Sepal width (cm)", title="6.3  |  KNN (k=5): Iris Classification")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.15)
fig.tight_layout()
out = Path("assets")
out.mkdir(exist_ok=True)
fig.savefig(out / "6_3_iris_knn.png", bbox_inches="tight", facecolor="white")
plt.show()
