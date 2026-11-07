import pandas as pd


def normalize_regions(values: pd.Series) -> pd.Series:
    lookup = {"seoul": "Seoul", "busan": "Busan", "gwangju": "Gwangju"}
    return values.astype("string").str.strip().str.casefold().map(lookup).astype("string")


if __name__ == "__main__":
    values = pd.Series([" seoul ", "BUSAN", "unknown"])
    print(normalize_regions(values).tolist())
