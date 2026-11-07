from pathlib import Path
import pandas as pd

source = Path(__file__).resolve().parents[1] / "data" / "regions.xlsx"
with pd.ExcelFile(source, engine="openpyxl") as excel:
    names = excel.sheet_names
    regions = pd.read_excel(excel, sheet_name="Regions", dtype={"region_code": "string"})
    targets = pd.read_excel(excel, sheet_name="Targets", dtype={"region_code": "string"})

print("Sheets:", ", ".join(names))
print("Regions:", len(regions))
print("First code:", regions.loc[0, "region_code"])
print("Total target:", int(targets["target_revenue"].sum()))
