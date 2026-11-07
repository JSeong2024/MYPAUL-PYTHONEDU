import pandas as pd


def missing_counts(frame: pd.DataFrame) -> pd.Series:
    normalized = frame.copy(deep=True)
    for column in normalized.select_dtypes(include=["object", "string"]).columns:
        normalized[column] = normalized[column].replace(r"^\s*$", pd.NA, regex=True)
    return normalized.isna().sum()


if __name__ == "__main__":
    demo = pd.DataFrame({"name": ["Kim", "  ", None], "score": [80, 90, None]})
    print(missing_counts(demo))
