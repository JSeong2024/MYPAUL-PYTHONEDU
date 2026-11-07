import pandas as pd


def add_revenue(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.assign(revenue_won=frame["quantity"] * frame["price_won"])


def summarize_by_region(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.groupby("region", as_index=False).agg(revenue_won=("revenue_won", "sum"))


orders = pd.DataFrame({"region": ["서울", "서울", "부산"], "quantity": [2, 1, 3], "price_won": [5000, 5000, 3000]})
report = orders.pipe(add_revenue).pipe(summarize_by_region)
print(report.sort_values("region").to_string(index=False))
