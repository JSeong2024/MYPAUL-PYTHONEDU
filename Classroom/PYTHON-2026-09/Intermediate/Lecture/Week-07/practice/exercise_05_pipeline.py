"""Exercise 05 | 비워 둔 TODO를 채우는 모델링 실습입니다.

이 파일은 학생용 과제입니다. 빈칸을 모두 완성한 뒤 실행하세요.
실행 시 친절한 안내를 위해 None을 사용하였으며, 아직 완성되지 않았을 때는 종료됩니다.
"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

iris = load_iris()
X = iris.data[:, 2:4]  # 꽃잎 길이와 너비
y = iris.target       # 정답: 0, 1, 2

# TODO 1: 평가용 비율(전체의 20%)을 숫자로 입력하세요.
TEST_SIZE = None
if TEST_SIZE is None:
    raise SystemExit("TODO 1: TEST_SIZE에 0.2를 입력한 뒤 다시 실행하세요.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=42, stratify=y
)
# KNN과 다른 분류 모델이지만 사용 순서는 동일: 생성 → fit() → predict() → 평가
model = DecisionTreeClassifier(random_state=42)

# TODO 2: 학습용 입력과 정답을 각각 지정하세요.
TRAIN_X = None
TRAIN_Y = None
if TRAIN_X is None or TRAIN_Y is None:
    raise SystemExit("TODO 2: TRAIN_X와 TRAIN_Y에 학습용 변수를 넣으세요.")
model.fit(TRAIN_X, TRAIN_Y)

# TODO 3: predict()에 입력할 평가용 입력 변수를 지정하세요.
TEST_X = None
if TEST_X is None:
    raise SystemExit("TODO 3: TEST_X에 평가용 입력 변수를 넣으세요.")
test_predictions = model.predict(TEST_X)

# TODO 4: 평가용 정답을 지정하세요.
TEST_Y = None
if TEST_Y is None:
    raise SystemExit("TODO 4: TEST_Y에 평가용 정답 변수를 넣으세요.")
print("Test Accuracy:", round(accuracy_score(TEST_Y, test_predictions), 3))
print("Confusion Matrix:\n", confusion_matrix(TEST_Y, test_predictions))
