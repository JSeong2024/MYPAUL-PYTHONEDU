import pandas as pd

orders = pd.DataFrame({"quantity": [2, 3, 4], "price": [5000, 7000, 2000]})
vectorized = orders["quantity"] * orders["price"]
row_loop = [row.quantity * row.price for row in orders.itertuples(index=False)]
assert vectorized.to_list() == row_loop
print("Revenue:", vectorized.to_list())
print("Memory bytes:", int(orders.memory_usage(deep=True).sum()))
