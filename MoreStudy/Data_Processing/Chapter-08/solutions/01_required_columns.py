"""Exercise 01 — 필수 열 검사 모범답안."""
import pandas as pd


def check_required_columns(df: pd.DataFrame, columns: list[str]) -> bool:
    return set(columns).issubset(df.columns)


if __name__ == "__main__":
    sample = pd.DataFrame({"station_id": ["ST-01"], "temperature_c": [21.0]})
    print(check_required_columns(sample, ["station_id", "temperature_c"]))
