"""Exercise 03 — 다대일 병합 후 미등록 상품을 거부하세요."""
import pandas as pd


def attach_category(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """product_id 기준 many_to_one, 미등록 키는 ValueError, 반환 시 category 포함."""
    # TODO: indicator/validate 사용, 원본 순서를 유지하세요.
    raise NotImplementedError


if __name__ == "__main__":
    orders = pd.DataFrame({"line_id": ["L1", "L2"], "product_id": ["P1", "P2"]})
    products = pd.DataFrame({"product_id": ["P1", "P2"], "category": ["디지털", "문구"]})
    print(attach_category(orders, products).to_string(index=False))
