from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path).set_index("order_id")
print("loc one:", orders.loc["ORD002", "product"])
print("loc slice:", orders.loc["ORD001":"ORD003", "product"].tolist())
print("iloc slice:", orders.iloc[0:3, 3].tolist())
print("iloc row positions:", orders.iloc[[0, 2]]["order_date"].tolist())
