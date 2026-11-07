from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
data = pd.read_csv(ROOT / "data/raw_orders.csv", dtype="string", keep_default_na=False)
data = data.apply(lambda column: column.str.strip().replace("", pd.NA))
print("Missing quantity:", int(data["quantity"].isna().sum()))
print("Missing region:", int(data["region"].isna().sum()))
print("Missing price:", int(data["unit_price"].isna().sum()))
