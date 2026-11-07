from pathlib import Path
import pandas as pd

source = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(
    source,
    dtype={"order_id": "string", "region_code": "string", "product_id": "string"},
    encoding="utf-8",
)
completed = orders.loc[orders["status"].eq("completed")].copy()
completed["revenue"] = completed["quantity"] * completed["unit_price"]

print("All orders:", len(orders))
print("Completed:", len(completed))
print("Revenue:", int(completed["revenue"].sum()))
print("First region:", orders.loc[0, "region_code"])
