"""Exercise 02. 같은 주문 ID가 반복되면 첫 레코드만 유지하세요."""
import pandas as pd


def deduplicate_orders(frame: pd.DataFrame) -> pd.DataFrame:
    # TODO: order_id 열을 기준으로 첫 행만 남기고 index를 재설정합니다.
    raise NotImplementedError


if __name__ == "__main__":
    demo = pd.DataFrame({"order_id": ["A", "B", "A"], "quantity": [1, 2, 3]})
    print(deduplicate_orders(demo))
