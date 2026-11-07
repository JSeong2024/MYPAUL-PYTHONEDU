from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
print("Shape:", orders.shape)
print("Columns:", orders.columns.tolist())
print("Order IDs:", orders.head(3)["order_id"].tolist())
print("Statuses:", sorted(orders["status"].unique().tolist()))
print("Quantity dtype:", orders["quantity"].dtype)
print("Quantity min/max:", orders["quantity"].min(), orders["quantity"].max())
print("Missing count:", int(orders.isna().sum().sum()))
