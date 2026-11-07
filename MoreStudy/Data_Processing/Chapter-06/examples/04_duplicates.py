import pandas as pd

orders = pd.DataFrame({
    "order_id": ["ORD-001", "ORD-002", "ORD-002"],
    "quantity": [1, 2, 4],
})
print("Exact row duplicates:", int(orders.duplicated().sum()))
print("Duplicate IDs:", int(orders.duplicated(subset=["order_id"]).sum()))
print("Kept first IDs:", orders.drop_duplicates(subset=["order_id"])["order_id"].tolist())
