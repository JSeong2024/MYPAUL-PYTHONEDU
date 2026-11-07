"""Exercise 03. 1~100 사이 양의 정수만 유효한 수량으로 처리하세요."""
import pandas as pd


def valid_quantity_mask(values: pd.Series) -> pd.Series:
    # TODO: 숫자가 아닌 값·소수·0·범위 밖의 값을 False로 처리합니다.
    raise NotImplementedError


if __name__ == "__main__":
    values = pd.Series(["1", "2.5", "-3", "100", "unknown"])
    print(valid_quantity_mask(values).tolist())
