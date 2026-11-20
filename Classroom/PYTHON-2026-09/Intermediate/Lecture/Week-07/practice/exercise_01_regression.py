"""Exercise 01 | 이동 거리→소요 시간 회귀 모델 실험. 값과 예측을 바꿔 보세요."""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

X = [[1], [2], [3], [4], [5], [6], [7], [8]]
y = [8, 13, 17, 23, 26, 32, 35, 41]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
pred_test = model.predict(X_test)
print(f"Test MAE: {mean_absolute_error(y_test, pred_test):.2f}분")
print(f"7km 예상 소요 시간: {model.predict([[7]])[0]:.1f}분")
# TODO: 9km를 입력한 예측값을 출력하고, 학습 범위 밖 예측의 한계를 설명하세요.
