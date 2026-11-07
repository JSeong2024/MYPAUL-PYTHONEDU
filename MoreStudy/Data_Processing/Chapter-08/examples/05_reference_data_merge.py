from pathlib import Path
import json
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
with (DATA / "stations.json").open(encoding="utf-8") as file:
    stations = pd.DataFrame(json.load(file))
measurements = pd.DataFrame({"station_id": ["ST-01", "ST-03"], "temperature_c": [19.5, 21.0]})
joined = measurements.merge(stations, on="station_id", how="left", validate="many_to_one", indicator=True)
assert joined["_merge"].eq("both").all()
print(joined[["station_id", "region", "temperature_c"]].to_string(index=False))
