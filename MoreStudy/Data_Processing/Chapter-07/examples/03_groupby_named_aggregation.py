import pandas as pd

orders = pd.DataFrame({
    "region": ["서울", "서울", "부산", "부산"],
    "order_id": ["O1", "O1", "O2", "O3"],
    "units": [2, 1, 3, 2],
    "sales_won": [20000, 10000, 15000, 14000],
})
summary = orders.groupby("region", as_index=False).agg(
    lines=("order_id", "size"),
    orders=("order_id", "nunique"),
    units=("units", "sum"),
    sales_won=("sales_won", "sum"),
).sort_values("region")
print(summary.to_string(index=False))
