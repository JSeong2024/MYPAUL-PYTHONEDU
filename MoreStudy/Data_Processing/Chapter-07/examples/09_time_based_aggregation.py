import pandas as pd

sales = pd.DataFrame({
    "date": pd.to_datetime(["2026-01-03", "2026-01-03", "2026-01-17", "2026-02-02"]),
    "sales_won": [10000, 5000, 22000, 8000],
})
daily = sales.set_index("date").resample("D")["sales_won"].sum()
monthly = sales.assign(month=sales["date"].dt.to_period("M").astype(str)).groupby("month")["sales_won"].sum()
print("Jan 3:", int(daily.loc["2026-01-03"]))
print("Jan 4:", int(daily.loc["2026-01-04"]))
print("Monthly:", monthly.to_dict())
