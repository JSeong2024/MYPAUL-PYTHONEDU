import pandas as pd


def parse_columns(raw: pd.DataFrame) -> pd.DataFrame:
    result = raw.copy()
    prices = result["price_text"].str.replace(",", "", regex=False)
    result["price"] = pd.to_numeric(prices, errors="coerce").astype("Int64")
    result["date"] = pd.to_datetime(result["date_text"], format="%Y-%m-%d", errors="coerce")
    return result
