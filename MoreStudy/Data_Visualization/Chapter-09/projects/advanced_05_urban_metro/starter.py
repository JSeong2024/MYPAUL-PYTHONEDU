"""Advanced Project 05 — Urban Transportation Dashboard (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def validate_boardings(*args, **kwargs):
    """Validate boardings."""
    raise NotImplementedError("validate_boardings: 해당 STEP을 구현하세요.")

def build_operating_slots(*args, **kwargs):
    """Build operating slots."""
    raise NotImplementedError("build_operating_slots: 해당 STEP을 구현하세요.")

def render_metro_dashboard(*args, **kwargs):
    """Render metro dashboard."""
    raise NotImplementedError("render_metro_dashboard: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Urban Transportation Dashboard")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "advanced_05_urban_metro")
    parser.add_argument("--line", default="")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
