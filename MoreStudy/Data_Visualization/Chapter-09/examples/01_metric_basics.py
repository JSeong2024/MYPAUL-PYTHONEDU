"""Example: P95, zero denominators, missing values."""
import pandas as pd
sample = pd.Series([100, 200, 300])
print('P95 (ms):', sample.quantile(0.95, interpolation='linear'))
values = pd.Series([0, None, 12])
print('Observed slots:', int(values.notna().sum()))
print('Known boardings:', float(values.sum()))
