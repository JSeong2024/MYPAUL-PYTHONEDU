import pandas as pd

january = pd.DataFrame({"order_id": ["O1", "O2"], "sales_won": [10000, 15000]})
february = pd.DataFrame({"order_id": ["O3"], "sales_won": [20000]})
combined = pd.concat([january, february], ignore_index=True)
print("Rows:", len(combined))

left = pd.Series([10, 20], index=["A", "B"])
right = pd.Series([5, 7], index=["B", "A"])
print("Aligned addition:", (left + right).to_dict())
