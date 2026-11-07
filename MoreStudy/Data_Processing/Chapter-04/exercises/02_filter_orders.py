import pandas as pd


def filter_orders(orders: pd.DataFrame, region: str, minimum_quantity: int) -> pd.DataFrame:
    """완료 상태·지정 지역·수량 이상 주문의 ID, 상품명, 수량을 반환하세요."""
    # 반환 컬럼: order_id, product, quantity / 기존 인덱스 초기화
    raise NotImplementedError
