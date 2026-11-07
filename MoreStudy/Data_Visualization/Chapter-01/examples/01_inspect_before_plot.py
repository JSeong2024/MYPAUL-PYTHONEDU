import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "park_visits.csv"
frame = pd.read_csv(DATA)

print("Rows:", len(frame))
print("Columns:", ", ".join(frame.columns))
print("Missing cells:", int(frame.isna().sum().sum()))
print("Duplicate dates:", int(frame["date"].duplicated().sum()))
print("Visitor range:", int(frame["visitors"].min()), "to", int(frame["visitors"].max()))
