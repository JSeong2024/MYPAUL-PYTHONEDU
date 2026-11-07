"""Exercise 03 — 모범답안."""
import pandas as pd


def attach_category(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    merged = orders.merge(products[["product_id", "category"]], on="product_id",
                          how="left", validate="many_to_one", indicator=True, sort=False)
    if merged["_merge"].ne("both").any():
        raise ValueError("Unknown product_id")
    return merged.drop(columns="_merge")


if __name__ == "__main__":
    orders = pd.DataFrame({"line_id": ["L1", "L2"], "product_id": ["P1", "P2"]})
    products = pd.DataFrame({"product_id": ["P1", "P2"], "category": ["디지털", "문구"]})
    print(attach_category(orders, products).to_string(index=False))
