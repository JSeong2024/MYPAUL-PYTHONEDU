import pandas as pd

values = pd.Series([18.0, None, 24.0, None, 30.0], name="temperature")
print("Valid measurements:", int(values.count()))
print("Drop missing:", values.dropna().tolist())
print("Fill with median:", values.fillna(values.median()).tolist())
print("Forward fill:", values.ffill().tolist())
