"""Challenge 03 — City Transit Reliability Platform (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def validate_reference_tables(*args, **kwargs):
    """Validate reference tables."""
    raise NotImplementedError("validate_reference_tables: 해당 STEP을 구현하세요.")

def audit_observations(*args, **kwargs):
    """Audit observations."""
    raise NotImplementedError("audit_observations: 해당 STEP을 구현하세요.")

def build_schedule_coverage(*args, **kwargs):
    """Build schedule coverage."""
    raise NotImplementedError("build_schedule_coverage: 해당 STEP을 구현하세요.")

def compare_incidents(*args, **kwargs):
    """Compare incidents."""
    raise NotImplementedError("compare_incidents: 해당 STEP을 구현하세요.")

def render_consistent_outputs(*args, **kwargs):
    """Render consistent outputs."""
    raise NotImplementedError("render_consistent_outputs: 해당 STEP을 구현하세요.")

def write_manifest(*args, **kwargs):
    """Write manifest."""
    raise NotImplementedError("write_manifest: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="City Transit Reliability Platform")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "challenge_03_transit_reliability")
    parser.add_argument("--start", default="2026-10-01")
    parser.add_argument("--end", default="2026-10-07")
    parser.add_argument("--line", default="")
    parser.add_argument("--stops", default="")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
