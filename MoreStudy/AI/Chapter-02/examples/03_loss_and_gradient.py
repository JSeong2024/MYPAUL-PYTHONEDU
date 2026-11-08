"""MSE의 기울기를 이용해 한 번의 Gradient Descent 갱신을 수행합니다."""
import numpy as np

x = np.array([0., 1., 2., 3.])
y = np.array([1., 3., 5., 7.])
w, b = 0.0, 0.0
learning_rate = 0.02

prediction = w * x + b
error = prediction - y
mse_before = float(np.mean(error ** 2))
grad_w = float(2 * np.mean(error * x))
grad_b = float(2 * np.mean(error))
w -= learning_rate * grad_w
b -= learning_rate * grad_b
mse_after = float(np.mean((w * x + b - y) ** 2))

print(f"Gradient: dw={grad_w:.2f}, db={grad_b:.2f}")
print(f"Updated: w={w:.2f}, b={b:.2f}")
print(f"MSE: {mse_before:.3f} -> {mse_after:.3f}")
