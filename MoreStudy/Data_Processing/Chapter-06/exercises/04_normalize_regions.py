"""Exercise 04. 허용 지역을 정규화하고 허용되지 않은 지역은 결측으로 처리하세요."""
import pandas as pd


def normalize_regions(values: pd.Series) -> pd.Series:
    # TODO: 공백·대소문자를 정리하고 Seoul/Busan/Gwangju만 반환합니다.
    raise NotImplementedError


if __name__ == "__main__":
    values = pd.Series([" seoul ", "BUSAN", "unknown"])
    print(normalize_regions(values).tolist())
