from pathlib import Path
import pandas as pd

file_path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(file_path)
indexed = orders.set_index("order_id")
renamed = indexed.rename(columns={"unit_price": "price_krw"})

print("Index name:", indexed.index.name)
print("First order product:", indexed.loc["ORD001", "product"])
print("Renamed:", "price_krw" in renamed.columns)
print("Restored index:", indexed.reset_index().columns[0])
print("Original unchanged:", "unit_price" in orders.columns)
