import pandas as pd

orders = pd.DataFrame({"store_id": ["S01", "S02", "S99"], "quantity": [2, 5, 1]})
store_names = {"S01": "서울점", "S02": "부산점"}
orders["store_name"] = orders["store_id"].map(store_names)
orders["size_class"] = "일반"
orders.loc[orders["quantity"] >= 4, "size_class"] = "대량"
print(orders.to_string(index=False))
print("Unknown store:", int(orders["store_name"].isna().sum()))
