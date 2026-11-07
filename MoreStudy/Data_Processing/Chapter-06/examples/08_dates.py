import pandas as pd

raw = pd.Series(["2026-10-01", "2026-02-30", "2026-10-03"], dtype="string")
parsed = pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
print("Valid dates:", int(parsed.notna().sum()))
print("Invalid dates:", int(parsed.isna().sum()))
