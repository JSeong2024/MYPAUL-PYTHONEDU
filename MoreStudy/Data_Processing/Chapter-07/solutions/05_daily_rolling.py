"""Exercise 05 — 모범답안."""
import pandas as pd


def daily_rolling_sum(frame: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    data = frame.copy()
    data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
    daily = data.groupby("date")["sales_won"].sum()
    dates = pd.date_range(start, end, freq="D")
    daily = daily.reindex(dates, fill_value=0)
    result = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"),
                           "sales_won": daily.to_numpy(),
                           "rolling_3d_sum": daily.rolling(window=3, min_periods=1).sum().astype("int64").to_numpy()})
    return result


if __name__ == "__main__":
    data = pd.DataFrame({"date": ["2026-01-01", "2026-01-03", "2026-01-03"], "sales_won": [100, 200, 50]})
    print(daily_rolling_sum(data, "2026-01-01", "2026-01-04").to_string(index=False))
