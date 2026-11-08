"""Advanced Project 04 — Regional Electricity Demand Analysis (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def validate_hourly_demand(*args, **kwargs):
    """Validate hourly demand."""
    raise NotImplementedError("validate_hourly_demand: 해당 STEP을 구현하세요.")

def convert_to_kst(*args, **kwargs):
    """Convert to kst."""
    raise NotImplementedError("convert_to_kst: 해당 STEP을 구현하세요.")

def build_energy_completeness(*args, **kwargs):
    """Build energy completeness."""
    raise NotImplementedError("build_energy_completeness: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Regional Electricity Demand Analysis")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "advanced_04_electricity_demand")
    parser.add_argument("--region", default="")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
