from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
orders = orders.assign(amount=lambda df: df["quantity"] * df["unit_price"])
orders["recognized_sales"] = 0
orders.loc[orders["status"] == "completed", "recognized_sales"] = orders.loc[
    orders["status"] == "completed", "amount"
]
print("All gross order amounts:", int(orders["amount"].sum()))
print("Recognized sales:", int(orders["recognized_sales"].sum()))
print("Canceled sales:", int(orders.loc[orders["status"] == "canceled", "recognized_sales"].sum()))
