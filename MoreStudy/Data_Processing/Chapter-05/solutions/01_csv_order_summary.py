from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

def summarize(path: Path) -> tuple[int, int]:
    orders = pd.read_csv(path, dtype={"order_id": "string", "region_code": "string"})
    completed = orders.loc[orders["status"].eq("completed")]
    revenue = (completed["quantity"] * completed["unit_price"]).sum()
    return len(completed), int(revenue)

if __name__ == "__main__":
    print(summarize(SOURCE))
