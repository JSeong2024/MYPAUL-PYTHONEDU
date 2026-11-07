import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.park_report import run_report

result = run_report(ROOT / "data" / "park_visits.csv", ROOT / "output" / "park_report")
print("Total days:", result["days"])
print("Total visitors:", result["total_visitors"])
print("Rainy days:", result["rainy_days"])
print("Saved charts:", 4)
