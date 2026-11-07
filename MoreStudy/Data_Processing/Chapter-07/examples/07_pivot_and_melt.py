import pandas as pd

long = pd.DataFrame({
    "store": ["서울", "서울", "부산", "부산"],
    "month": ["2026-01", "2026-02", "2026-01", "2026-02"],
    "sales_won": [30000, 41000, 25000, 38000],
})
wide = long.pivot(index="store", columns="month", values="sales_won")
round_trip = wide.reset_index().melt(id_vars="store", var_name="month", value_name="sales_won")
print(wide.to_string())
print("Recovered rows:", len(round_trip))
