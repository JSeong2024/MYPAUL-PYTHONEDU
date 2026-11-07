"""Exercise 02 — 지역별 주문 행 수, 수량, 매출 합계를 계산하세요."""
import pandas as pd


def summarize_region(frame: pd.DataFrame) -> pd.DataFrame:
    """region별 line_count(size), units(sum quantity), sales_won(sum)을 region 오름차순 반환."""
    # TODO: groupby + named aggregation
    raise NotImplementedError


if __name__ == "__main__":
    data = pd.DataFrame({"region": ["서울", "서울", "부산"], "quantity": [2, 1, 3], "sales_won": [10000, 5000, 9000]})
    print(summarize_region(data).to_string(index=False))
