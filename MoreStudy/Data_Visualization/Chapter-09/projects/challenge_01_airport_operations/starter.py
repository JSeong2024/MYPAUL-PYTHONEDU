"""Challenge 01 — Airport Operations Analysis (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def audit_flights(*args, **kwargs):
    """Audit flights."""
    raise NotImplementedError("audit_flights: 해당 STEP을 구현하세요.")

def compute_airport_metrics(*args, **kwargs):
    """Compute airport metrics."""
    raise NotImplementedError("compute_airport_metrics: 해당 STEP을 구현하세요.")

def render_airport_report(*args, **kwargs):
    """Render airport report."""
    raise NotImplementedError("render_airport_report: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Airport Operations Analysis")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "challenge_01_airport_operations")
    parser.add_argument("--start", default="2026-10-01")
    parser.add_argument("--end", default="2026-10-07")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
