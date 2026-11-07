import pandas as pd

observed = pd.Series(
    [1000, 2000],
    index=pd.to_datetime(["2026-01-01", "2026-01-03"]),
)
calendar = pd.date_range("2026-01-01", "2026-01-04", freq="D")
unknown = observed.reindex(calendar)
zero_assumed = unknown.fillna(0).astype("int64")
print("Missing before assumption:", int(unknown.isna().sum()))
print("After zero-fill:", zero_assumed.to_list())
