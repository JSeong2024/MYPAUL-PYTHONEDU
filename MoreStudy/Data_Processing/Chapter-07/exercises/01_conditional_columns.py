"""Exercise 01 — 조건별 매출 구간을 계산하세요."""
import pandas as pd


def classify_sales(orders: pd.DataFrame) -> pd.DataFrame:
    """quantity * unit_price_won으로 sales_won, 30000 이상은 '대량', 미만은 '일반'."""
    # TODO: 원본을 변경하지 않고 필요한 열을 추가하여 반환하세요.
    raise NotImplementedError


if __name__ == "__main__":
    data = pd.DataFrame({"quantity": [2, 4, 1], "unit_price_won": [10000, 10000, 5000]})
    print(classify_sales(data).to_string(index=False))
