from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
raw = pd.read_csv(DATA / "weather_observations.csv", dtype=str, keep_default_na=False)
converted = pd.to_numeric(raw["temperature_c"], errors="coerce")
timestamps = pd.to_datetime(raw["timestamp_local"], format="%Y-%m-%d %H:%M", errors="coerce")
print("Unparseable/missing temperatures:", int(converted.isna().sum()))
print("Invalid timestamps:", int(timestamps.isna().sum()))
print("Finite temperatures:", int((converted.notna() & converted.between(-30, 45)).sum()))
