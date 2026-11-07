import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean, make_summaries

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
_, _, monthly, _ = make_summaries(clean, stations, policy)
print(monthly[["year_month", "region", "readings", "avg_temperature_c"]].to_string(index=False))
