import pandas as pd


def category_summary(orders: pd.DataFrame) -> pd.DataFrame:
    completed = orders.loc[orders["status"] == "completed"].copy()
    completed["amount"] = completed["quantity"] * completed["unit_price"]
    summary = completed.groupby("category", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    )
    return summary.sort_values(["revenue", "category"], ascending=[False, True]).reset_index(drop=True)
