"""Exercise 02 — 기온 검증 모범답안."""
import numpy as np
import pandas as pd


def temperature_status(values: pd.Series) -> pd.DataFrame:
    numbers = pd.to_numeric(values, errors="coerce")
    valid = numbers.notna() & np.isfinite(numbers) & numbers.between(-30, 45)
    return pd.DataFrame({"value": numbers.to_numpy(), "valid": valid.to_numpy(dtype=bool)})


if __name__ == "__main__":
    sample = pd.Series(["21.5", "", "68", "invalid"])
    print(temperature_status(sample).to_string(index=False))
