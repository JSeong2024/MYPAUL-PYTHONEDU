from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
mask = (orders["status"] == "completed") & (orders["region"] == "서울")
seoul = orders.loc[mask, ["order_id", "product", "quantity"]]
print("Seoul completed:", len(seoul))
print(seoul.to_string(index=False))
print("In Seoul or Busan:", int(orders["region"].isin(["서울", "부산"]).sum()))
