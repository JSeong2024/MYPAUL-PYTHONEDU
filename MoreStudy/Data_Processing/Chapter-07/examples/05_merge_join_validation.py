import pandas as pd

orders = pd.DataFrame({"line_id": ["L1", "L2", "L3"], "product_id": ["P1", "P2", "PX"]})
products = pd.DataFrame({"product_id": ["P1", "P2"], "category": ["디지털", "문구"]})
merged = orders.merge(products, on="product_id", how="left", validate="many_to_one", indicator=True)
print(merged[["line_id", "product_id", "category", "_merge"]].to_string(index=False))
print("Unmatched:", int(merged["_merge"].eq("left_only").sum()))
