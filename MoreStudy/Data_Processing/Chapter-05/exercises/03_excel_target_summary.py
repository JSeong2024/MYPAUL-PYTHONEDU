"""Exercise 03: Excel의 Targets 시트에서 목표 매출 합계를 계산하세요."""
from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "data" / "regions.xlsx"

def total_target(path: Path) -> int:
    # TODO: Targets 시트를 읽고 target_revenue 열을 합산합니다.
    raise NotImplementedError

if __name__ == "__main__":
    print(total_target(SOURCE))
