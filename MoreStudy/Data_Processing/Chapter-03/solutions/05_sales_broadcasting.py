"""Solution 05 — 날짜별 판매 수량 행렬과 가격 배열로 매출 계산."""
import numpy as np

def daily_sales(quantities: np.ndarray, prices: np.ndarray) -> np.ndarray:
    qty = np.asarray(quantities)
    unit_prices = np.asarray(prices)
    if qty.ndim != 2 or unit_prices.ndim != 1 or qty.shape[1] != unit_prices.size:
        raise ValueError("입력 shape가 맞지 않습니다.")
    if 0 in qty.shape:
        raise ValueError("판매 데이터가 비어 있습니다.")
    return (qty * unit_prices).sum(axis=1)

if __name__ == "__main__":
    qty = np.array([[2, 1, 0], [0, 3, 1]])
    print(daily_sales(qty, np.array([1000, 2000, 1500])))
