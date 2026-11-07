import pandas as pd


def build_dataframe() -> pd.DataFrame:
    return pd.DataFrame({"product": ["커피", "노트", "펜"], "quantity": [2, 3, 5], "unit_price": [3500, 2500, 1000]})


if __name__ == "__main__":
    print(build_dataframe().to_string(index=False))
