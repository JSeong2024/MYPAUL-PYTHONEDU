from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
orders["order_date"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d")
print("October orders:", int(orders["order_date"].dt.month.eq(10).sum()))
print("Products containing '커':", orders.loc[orders["product"].str.contains("커", regex=False), "product"].unique().tolist())
print("Earliest date:", orders["order_date"].min().date())
