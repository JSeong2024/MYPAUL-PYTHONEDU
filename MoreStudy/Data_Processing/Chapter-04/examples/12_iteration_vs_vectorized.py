from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
values = [row.quantity * row.unit_price for row in orders.itertuples(index=False)]
vectorized = (orders["quantity"] * orders["unit_price"]).tolist()
print("Same results:", values == vectorized)
print("Row count:", len(values))
print("First 3 amounts:", vectorized[:3])
