"""Advanced Project 01 — Weather Monitoring Dashboard (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def validate_observations(*args, **kwargs):
    """Validate observations."""
    raise NotImplementedError("validate_observations: 해당 STEP을 구현하세요.")

def build_expected_calendar(*args, **kwargs):
    """Build expected calendar."""
    raise NotImplementedError("build_expected_calendar: 해당 STEP을 구현하세요.")

def draw_station_comparison(*args, **kwargs):
    """Draw station comparison."""
    raise NotImplementedError("draw_station_comparison: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Weather Monitoring Dashboard")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "advanced_01_weather_dashboard")
    parser.add_argument("--start", default="2026-10-01")
    parser.add_argument("--end", default="2026-10-07")
    parser.add_argument("--stations", default="")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
