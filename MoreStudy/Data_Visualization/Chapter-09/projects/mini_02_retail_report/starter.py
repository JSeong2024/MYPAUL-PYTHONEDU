"""Mini Project 02 — Retail Sales Performance Report (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def read_orders(*args, **kwargs):
    """Read orders."""
    raise NotImplementedError("read_orders: 해당 STEP을 구현하세요.")

def summarize_completed_sales(*args, **kwargs):
    """Summarize completed sales."""
    raise NotImplementedError("summarize_completed_sales: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Retail Sales Performance Report")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "mini_02_retail_report")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
