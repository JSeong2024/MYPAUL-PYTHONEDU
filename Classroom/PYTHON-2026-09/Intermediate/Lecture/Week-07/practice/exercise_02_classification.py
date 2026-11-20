"""Exercise 02 | 검증 데이터로 KNN의 K 값을 비교합니다. Test는 마지막에만 사용합니다."""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
X, y = iris.data[:, :2], iris.target
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=42, stratify=y_dev)

scores = {}
for k in [1, 3, 5, 7]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    scores[k] = accuracy_score(y_val, model.predict(X_val))
    print(f"K={k}: Validation Accuracy={scores[k]:.3f}")

best_k = max(scores, key=scores.get)
final_model = KNeighborsClassifier(n_neighbors=best_k)
final_model.fit(X_dev, y_dev)
print(f"선택된 K={best_k}")
print(f"Final Test Accuracy: {accuracy_score(y_test, final_model.predict(X_test)):.3f}")
# TODO: K가 커질수록 점수가 항상 높아지는지 설명하세요.
