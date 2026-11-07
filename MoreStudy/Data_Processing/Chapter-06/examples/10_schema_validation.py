import pandas as pd

required = {"order_id", "quantity", "unit_price"}
frame = pd.DataFrame({"order_id": ["ORD-001"], "quantity": [2]})
missing = sorted(required - set(frame.columns))
print("Missing columns:", missing)
print("Schema valid:", not missing)
