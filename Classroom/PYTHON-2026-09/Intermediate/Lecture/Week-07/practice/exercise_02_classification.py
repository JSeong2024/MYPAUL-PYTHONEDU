"""Exercise 02 | KNN 설정 바꿔보기 — TODO에 맞추어 코드를 완성할 것."""
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data[:, :2]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# TODO 1: n_neighbors를 1, 3, 5, 7로 바꿔 각각 학습
# TODO 2: 각 모델의 테스트 정확도 기록
# TODO 3: 정확도가 달라지는 이유를 한 문장으로 설명

print("TODO: 이웃 수를 바꾸어 결과를 비교해 보세요.")
