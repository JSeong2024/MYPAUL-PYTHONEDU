"""Build figures and reports from the synthetic library visits dataset."""

import argparse
from pathlib import Path
from project.chart_design import load_visits, make_report

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Library chart design review")
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "library_visits.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    info = make_report(load_visits(args.input), args.output)
    print(f"Rows: {info['source_rows']}/{info['expected_rows']} expected")
    print(f"Missing records: {info['missing_records']}")
    print(f"Total visitors: {info['total_visitors']:,}")
    print(f"New memberships: {info['total_new_members']:,}")
    print(f"Charts saved: {len(info['figure_files'])}")


if __name__ == "__main__":
    main()
