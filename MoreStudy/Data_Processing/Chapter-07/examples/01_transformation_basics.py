import pandas as pd

orders = pd.DataFrame({
    "order_id": ["A1", "A2", "A3"],
    "quantity": [2, 3, 1],
    "unit_price_won": [10000, 5000, 12000],
})
orders = orders.assign(sales_won=orders["quantity"] * orders["unit_price_won"])
orders = orders.rename(columns={"sales_won": "gross_sales_won"})
print(orders[["order_id", "gross_sales_won"]].to_string(index=False))
