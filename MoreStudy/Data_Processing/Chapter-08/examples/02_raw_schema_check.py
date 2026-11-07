from pathlib import Path
import csv
import json

DATA = Path(__file__).resolve().parents[1] / "data"
with (DATA / "weather_observations.csv").open(encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    columns = reader.fieldnames or []
with (DATA / "stations.json").open(encoding="utf-8") as file:
    stations = json.load(file)
print("CSV fields:", len(columns))
print("Station IDs:", [row["station_id"] for row in stations])
print("Unique station IDs:", len({row["station_id"] for row in stations}) == len(stations))
