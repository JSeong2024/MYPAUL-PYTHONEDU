"""출력의 형태에 따라 Regression과 Classification을 구별한다."""
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression

X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
y_reg = np.array([2.4, 4.2, 6.3, 8.1, 10.2, 12.1])
y_cls = np.array([0, 0, 0, 1, 1, 1])

regressor = LinearRegression().fit(X, y_reg)
classifier = LogisticRegression().fit(X, y_cls)
new_x = np.array([[3.5]])
print(f"Regression: {regressor.predict(new_x)[0]:.2f}")
print(f"Classification: {classifier.predict(new_x)[0]}")
print(f"Class 1 probability estimate: {classifier.predict_proba(new_x)[0, 1]:.3f}")
