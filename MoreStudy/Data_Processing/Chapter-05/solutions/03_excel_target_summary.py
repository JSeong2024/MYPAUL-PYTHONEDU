from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "data" / "regions.xlsx"

def total_target(path: Path) -> int:
    targets = pd.read_excel(path, sheet_name="Targets", engine="openpyxl", dtype={"region_code": "string"})
    return int(targets["target_revenue"].sum())

if __name__ == "__main__":
    print(total_target(SOURCE))
