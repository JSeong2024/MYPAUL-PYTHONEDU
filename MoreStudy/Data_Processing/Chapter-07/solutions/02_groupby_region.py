"""Exercise 02 — 모범답안."""
import pandas as pd


def summarize_region(frame: pd.DataFrame) -> pd.DataFrame:
    return (frame.groupby("region", as_index=False).agg(
        line_count=("region", "size"), units=("quantity", "sum"),
        sales_won=("sales_won", "sum"),
    ).sort_values("region").reset_index(drop=True))


if __name__ == "__main__":
    data = pd.DataFrame({"region": ["서울", "서울", "부산"], "quantity": [2, 1, 3], "sales_won": [10000, 5000, 9000]})
    print(summarize_region(data).to_string(index=False))
