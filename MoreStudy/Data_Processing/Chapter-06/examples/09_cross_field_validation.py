import pandas as pd

orders = pd.DataFrame({
    "status": ["completed", "cancelled", "completed"],
    "quantity": [2, 1, 0],
    "unit_price": [1500, 2000, 5000],
})
valid_qty = orders["quantity"].gt(0)
revenue = orders.loc[valid_qty & orders["status"].eq("completed"), "quantity"] * orders["unit_price"]
print("Invalid quantity:", int((~valid_qty).sum()))
print("Completed revenue:", int(revenue.sum()))
