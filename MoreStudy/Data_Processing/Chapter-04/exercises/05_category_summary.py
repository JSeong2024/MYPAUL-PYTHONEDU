import pandas as pd


def category_summary(orders: pd.DataFrame) -> pd.DataFrame:
    """완료 주문을 분류별로 집계하고 매출액이 큰 순서로 반환하세요."""
    # 반환 컬럼: category, orders(건수), revenue(매출액)
    # 매출 동률일 때 category 오름차순, 결과 인덱스 초기화
    raise NotImplementedError
