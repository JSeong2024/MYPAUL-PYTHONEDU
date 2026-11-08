"""Challenge 02 — Energy Demand & Anomaly Detection (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def build_expected_hours(*args, **kwargs):
    """Build expected hours."""
    raise NotImplementedError("build_expected_hours: 해당 STEP을 구현하세요.")

def detect_hourly_anomalies(*args, **kwargs):
    """Detect hourly anomalies."""
    raise NotImplementedError("detect_hourly_anomalies: 해당 STEP을 구현하세요.")

def match_incident_intervals(*args, **kwargs):
    """Match incident intervals."""
    raise NotImplementedError("match_incident_intervals: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Energy Demand & Anomaly Detection")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "challenge_02_energy_anomalies")
    parser.add_argument("--region", default="")
    parser.add_argument("--threshold-mw", type=float, default=120.0)
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
