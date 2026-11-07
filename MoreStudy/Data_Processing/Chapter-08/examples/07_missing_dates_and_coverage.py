import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean, make_summaries

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
_, _, _, coverage = make_summaries(clean, stations, policy)
print("Coverage counts:", coverage["status"].value_counts().sort_index().to_dict())
missing = coverage.loc[coverage["status"].eq("missing"), ["station_id", "date"]]
print(missing.to_string(index=False))
