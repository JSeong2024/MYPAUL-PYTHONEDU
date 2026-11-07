import json
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
source = root / "data" / "orders.csv"
output = root / "output" / "orders.json"
orders = pd.read_csv(source, dtype={"region_code": "string"})
output.parent.mkdir(parents=True, exist_ok=True)
orders.to_json(output, orient="records", force_ascii=False, indent=2)

converted = json.loads(output.read_text(encoding="utf-8"))
print("Exported:", len(converted))
print("Region code:", converted[0]["region_code"])
