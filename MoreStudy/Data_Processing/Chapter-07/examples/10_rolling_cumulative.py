import pandas as pd

sales = pd.Series([100, 0, 300, 200, 400], index=pd.date_range("2026-01-01", periods=5, freq="D"))
rolling = sales.rolling(window=3, min_periods=1).mean()
cumulative = sales.cumsum()
print("Day 3 moving average:", float(rolling.iloc[2]))
print("Day 5 cumulative:", int(cumulative.iloc[-1]))
