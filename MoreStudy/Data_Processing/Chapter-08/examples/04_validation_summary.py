import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean

raw, stations, policy = load_inputs(ROOT / "data")
clean, issues, audit = validate_and_clean(raw, stations, policy)
print("Statuses:", audit["status"].value_counts().sort_index().to_dict())
print("Issue rows:", len(issues))
print("Clean rows:", len(clean))
