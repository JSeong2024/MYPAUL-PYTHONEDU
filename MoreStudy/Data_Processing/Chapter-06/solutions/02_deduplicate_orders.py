import pandas as pd


def deduplicate_orders(frame: pd.DataFrame) -> pd.DataFrame:
    if "order_id" not in frame.columns:
        raise ValueError("order_id column is required")
    return frame.drop_duplicates(subset=["order_id"], keep="first").reset_index(drop=True)


if __name__ == "__main__":
    demo = pd.DataFrame({"order_id": ["A", "B", "A"], "quantity": [1, 2, 3]})
    print(deduplicate_orders(demo))
