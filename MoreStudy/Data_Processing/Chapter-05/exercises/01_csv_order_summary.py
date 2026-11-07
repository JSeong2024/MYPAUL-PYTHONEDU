"""Exercise 01: 원본 CSV에서 완료 주문 수 및 합계 매출을 계산하세요."""
from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

def summarize(path: Path) -> tuple[int, int]:
    # TODO: 주문 코드와 지역 코드를 문자열로 읽습니다.
    # TODO: 완료(completed) 주문만 골라 수량 × 단가를 합산합니다.
    raise NotImplementedError

if __name__ == "__main__":
    print(summarize(SOURCE))
