import pandas as pd


def top_revenue_orders(orders: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """완료된 주문 중 매출액이 큰 n건을 반환하세요."""
    # 매출액 = quantity * unit_price, 동률이면 order_id 오름차순
    # 반환 컬럼: order_id, amount / 인덱스 0부터 시작
    raise NotImplementedError
