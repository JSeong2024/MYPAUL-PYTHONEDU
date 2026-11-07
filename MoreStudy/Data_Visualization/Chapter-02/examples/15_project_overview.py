from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.chart_design import load_visits, branch_summary, completeness

frame = load_visits(ROOT / "data" / "library_visits.csv")
summary = branch_summary(frame)
coverage = completeness(frame)
print("Observed:", len(frame), "Expected:", len(coverage))
print("Missing:", int((~coverage["observed"]).sum()))
print("Overall visitors:", int(summary["visitors"].sum()))
print("Branch totals:", summary.set_index("branch")["visitors"].to_dict())
