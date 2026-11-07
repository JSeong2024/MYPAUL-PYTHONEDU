from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.chart_design import load_visits, make_report

result = make_report(load_visits(ROOT / "data" / "library_visits.csv"), ROOT / "output")
print("Visitors:", result["total_visitors"])
print("Missing:", result["missing_records"])
print("Images:", len(result["figure_files"]))
