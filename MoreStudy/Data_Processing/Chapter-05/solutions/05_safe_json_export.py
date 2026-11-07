import json
from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

def convert(source: Path, destination: Path) -> int:
    orders = pd.read_csv(source, dtype={"region_code": "string"})
    completed = orders.loc[orders["status"].eq("completed")].copy()
    destination.parent.mkdir(parents=True, exist_ok=True)
    completed.to_json(destination, orient="records", force_ascii=False, indent=2)
    with destination.open("r", encoding="utf-8") as file:
        records = json.load(file)
    return len(records)

if __name__ == "__main__":
    destination = Path(__file__).resolve().parents[1] / "output" / "exercise05.json"
    print(convert(SOURCE, destination))
