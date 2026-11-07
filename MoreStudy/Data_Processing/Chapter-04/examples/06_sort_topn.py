from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
completed = orders.loc[orders["status"] == "completed"].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
top3 = completed.sort_values(["amount", "order_id"], ascending=[False, True]).head(3)
print(top3[["order_id", "amount"]].to_string(index=False))
