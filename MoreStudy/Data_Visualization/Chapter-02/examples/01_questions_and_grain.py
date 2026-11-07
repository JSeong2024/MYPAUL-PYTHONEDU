from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
frame = pd.read_csv(ROOT / "data" / "library_visits.csv", parse_dates=["date"])

print("Rows:", len(frame))
print("Unique branches:", frame["branch"].nunique())
print("Unique dates:", frame["date"].nunique())
print("Duplicate branch/date keys:", int(frame.duplicated(["branch", "date"]).sum()))
