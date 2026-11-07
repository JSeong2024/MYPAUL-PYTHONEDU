import pandas as pd

prices = pd.Series([12, 14, 15, 15, 16, 18, 19, 21, 100])
q1, q3 = prices.quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
flagged = prices.loc[~prices.between(lower, upper)]
print(f"IQR bounds: {lower:.1f} to {upper:.1f}")
print("Review candidates:", flagged.tolist())
