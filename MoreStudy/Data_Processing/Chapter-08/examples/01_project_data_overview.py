from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
raw = pd.read_csv(DATA / "weather_observations.csv", dtype=str, keep_default_na=False)
print("Rows:", len(raw))
print("Columns:", ", ".join(raw.columns))
print("Stations (raw):", sorted(raw["station_id"].unique().tolist()))
