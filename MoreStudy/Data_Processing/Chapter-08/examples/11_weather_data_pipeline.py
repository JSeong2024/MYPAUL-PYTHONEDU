import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import run_pipeline

result = run_pipeline(ROOT / "data", ROOT / "output")
report = result.report
print(f"Raw: {report['total_raw_rows']} | Accepted: {report['accepted_rows']} | "
      f"Review: {report['review_rows']} | Rejected: {report['rejected_rows']}")
print(f"Coverage: {report['valid_observations']}/{report['expected_observation_slots']} "
      f"({report['coverage_pct']:.2f}%)")
