from pathlib import Path
import pandas as pd

chapter = Path(__file__).resolve().parents[1]
orders = pd.read_csv(chapter / "data" / "orders.csv")
completed = orders.loc[orders["status"] == "completed", ["order_id", "region", "quantity", "unit_price"]].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
output_path = chapter / "output" / "completed_orders.csv"
output_path.parent.mkdir(exist_ok=True)
completed.to_csv(output_path, index=False, encoding="utf-8")
reloaded = pd.read_csv(output_path)
print("Saved:", output_path.name)
print("Saved rows:", len(reloaded))
print("Total amount:", int(reloaded["amount"].sum()))
