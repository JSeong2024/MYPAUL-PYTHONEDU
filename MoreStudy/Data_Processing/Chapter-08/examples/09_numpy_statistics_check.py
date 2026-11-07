import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
values = clean.loc[clean["station_id"].eq("ST-01"), "temperature_c"].to_numpy(dtype=float)
print("Records:", len(values))
print("NumPy mean:", round(float(np.mean(values)), 2))
print("Pandas mean:", round(float(clean.loc[clean["station_id"].eq("ST-01"), "temperature_c"].mean()), 2))
