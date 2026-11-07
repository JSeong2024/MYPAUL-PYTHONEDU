"""Exercise 05 — 날짜별 판매 수량 행렬과 가격 배열로 매출 계산."""
import numpy as np

def daily_sales(quantities: np.ndarray, prices: np.ndarray) -> np.ndarray:
    """날짜별 총매출을 1차원 배열로 반환합니다."""
    # TODO: quantities는 (날짜 수, 상품 수), prices는 (상품 수,)입니다.
    # TODO: 잘못된 shape에는 ValueError를 발생시킵니다.
    # TODO: 각 날짜의 합계를 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    qty = np.array([[2, 1, 0], [0, 3, 1]])
    print(daily_sales(qty, np.array([1000, 2000, 1500])))
