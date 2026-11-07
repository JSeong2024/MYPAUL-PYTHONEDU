from importlib.util import find_spec
from pathlib import Path
import pandas as pd

if find_spec("pyarrow") is None:
    print("PyArrow가 필요합니다: python -m pip install pyarrow")
else:
    root = Path(__file__).resolve().parents[1]
    orders = pd.read_csv(root / "data" / "orders.csv", dtype={"region_code": "string"})
    destination = root / "output" / "orders.parquet"
    destination.parent.mkdir(parents=True, exist_ok=True)
    orders.to_parquet(destination, engine="pyarrow", compression="snappy", index=False)
    selected = pd.read_parquet(destination, engine="pyarrow", columns=["order_id", "region_code"])
    print("Rows:", len(selected))
    print("Columns:", ", ".join(selected.columns))
