"""Exercise 05: CSV의 완료 주문을 JSON으로 저장하고 다시 읽어 건수를 확인하세요."""
import json
from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "data" / "orders.csv"

def convert(source: Path, destination: Path) -> int:
    # TODO: 완료 주문만 선택하고 destination을 생성합니다.
    # TODO: 선행 0을 가진 region_code를 문자열로 보존합니다.
    # TODO: JSON을 다시 읽고 항목 수를 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    destination = Path(__file__).resolve().parents[1] / "output" / "exercise05.json"
    print(convert(SOURCE, destination))
