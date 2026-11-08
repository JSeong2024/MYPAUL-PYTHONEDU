"""Advanced Project 03 — Service Performance Monitoring (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def validate_requests(*args, **kwargs):
    """Validate requests."""
    raise NotImplementedError("validate_requests: 해당 STEP을 구현하세요.")

def filter_kst_requests(*args, **kwargs):
    """Filter kst requests."""
    raise NotImplementedError("filter_kst_requests: 해당 STEP을 구현하세요.")

def compute_latency_metrics(*args, **kwargs):
    """Compute latency metrics."""
    raise NotImplementedError("compute_latency_metrics: 해당 STEP을 구현하세요.")

def build_service_dashboard(*args, **kwargs):
    """Build service dashboard."""
    raise NotImplementedError("build_service_dashboard: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Service Performance Monitoring")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "advanced_03_service_monitor")
    parser.add_argument("--start", default="2026-10-01")
    parser.add_argument("--end", default="2026-10-07")
    parser.add_argument("--services", default="")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
