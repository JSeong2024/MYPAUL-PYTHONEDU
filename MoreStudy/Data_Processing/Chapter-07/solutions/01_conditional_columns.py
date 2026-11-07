"""Exercise 01 — 모범답안."""
import pandas as pd


def classify_sales(orders: pd.DataFrame) -> pd.DataFrame:
    result = orders.copy()
    result["sales_won"] = result["quantity"] * result["unit_price_won"]
    result["size_class"] = "일반"
    result.loc[result["sales_won"] >= 30000, "size_class"] = "대량"
    return result


if __name__ == "__main__":
    data = pd.DataFrame({"quantity": [2, 4, 1], "unit_price_won": [10000, 10000, 5000]})
    print(classify_sales(data).to_string(index=False))
