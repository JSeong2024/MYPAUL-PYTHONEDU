import pandas as pd


def filter_orders(orders: pd.DataFrame, region: str, minimum_quantity: int) -> pd.DataFrame:
    mask = (
        (orders["status"] == "completed")
        & (orders["region"] == region)
        & (orders["quantity"] >= minimum_quantity)
    )
    return orders.loc[mask, ["order_id", "product", "quantity"]].reset_index(drop=True)
