import pandas as pd


def valid_quantity_mask(values: pd.Series) -> pd.Series:
    numbers = pd.to_numeric(values, errors="coerce")
    return (
        numbers.notna() & numbers.between(1, 100) &
        numbers.mod(1).eq(0)
    ).fillna(False).astype(bool)


if __name__ == "__main__":
    values = pd.Series(["1", "2.5", "-3", "100", "unknown"])
    print(valid_quantity_mask(values).tolist())
