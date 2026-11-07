from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
completed = orders.loc[orders["status"] == "completed"].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
summary = completed.groupby("region", as_index=False).agg(
    order_count=("order_id", "size"), sales=("amount", "sum")
).sort_values("region")
print(summary.to_string(index=False))
