import pandas as pd


def top_revenue_orders(orders: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    if n < 0:
        raise ValueError("n must not be negative")
    selected = orders.loc[orders["status"] == "completed"].copy()
    selected["amount"] = selected["quantity"] * selected["unit_price"]
    return (selected.sort_values(["amount", "order_id"], ascending=[False, True])
            .head(n)[["order_id", "amount"]].reset_index(drop=True))
