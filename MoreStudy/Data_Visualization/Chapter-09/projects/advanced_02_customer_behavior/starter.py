"""Advanced Project 02 — Customer Behavior Analysis (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def audit_orders(*args, **kwargs):
    """Audit orders."""
    raise NotImplementedError("audit_orders: 해당 STEP을 구현하세요.")

def segment_participation(*args, **kwargs):
    """Segment participation."""
    raise NotImplementedError("segment_participation: 해당 STEP을 구현하세요.")

def draw_segment_dashboard(*args, **kwargs):
    """Draw segment dashboard."""
    raise NotImplementedError("draw_segment_dashboard: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Customer Behavior Analysis")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "advanced_02_customer_behavior")
    parser.add_argument("--start", default="2026-10-01")
    parser.add_argument("--end", default="2026-10-07")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
