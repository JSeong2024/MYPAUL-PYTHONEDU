import pandas as pd

orders = pd.DataFrame({
    "order_id": ["ORD-001", "ORD-002", "ORD-002"],
    "quantity": [2, None, 3],
    "unit_price": [1500, 2500, -5],
})
print("Rows:", len(orders))
print("Missing quantity:", int(orders["quantity"].isna().sum()))
print("Duplicate order ID:", int(orders["order_id"].duplicated().sum()))
print("Invalid unit price:", int((orders["unit_price"] <= 0).sum()))
