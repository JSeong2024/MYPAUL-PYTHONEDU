"""Regression의 오차 크기와 R²를 계산한다."""
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_true = np.array([20., 25., 35., 40.])
y_pred = np.array([18., 29., 32., 39.])
errors = y_true - y_pred
mae = np.abs(errors).mean()
mse = (errors ** 2).mean()
rmse = np.sqrt(mse)
r2 = 1 - (errors ** 2).sum() / ((y_true-y_true.mean()) ** 2).sum()
print(f"MAE={mae:.3f}, MSE={mse:.3f}, RMSE={rmse:.3f}, R²={r2:.3f}")
assert np.isclose(mae, mean_absolute_error(y_true, y_pred))
assert np.isclose(mse, mean_squared_error(y_true, y_pred))
assert np.isclose(r2, r2_score(y_true, y_pred))
