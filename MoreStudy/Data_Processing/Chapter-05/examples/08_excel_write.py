from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
source = root / "data" / "regions.xlsx"
output = root / "output" / "region_targets_copy.xlsx"
regions = pd.read_excel(source, sheet_name="Regions", dtype={"region_code": "string"}, engine="openpyxl")
targets = pd.read_excel(source, sheet_name="Targets", dtype={"region_code": "string"}, engine="openpyxl")

output.parent.mkdir(parents=True, exist_ok=True)
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    regions.to_excel(writer, sheet_name="Regions", index=False)
    targets.to_excel(writer, sheet_name="Targets", index=False)
print("Saved:", output.name)
print("Sheets: 2")
