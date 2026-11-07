"""Exercise 02 — 기온 자료형 변환과 검증을 구현하세요."""
import pandas as pd


def temperature_status(values: pd.Series) -> pd.DataFrame:
    """[-30, 45] 범위 유효 여부를 반환하세요.

    반환 열: value(숫자 또는 NaN), valid(bool).
    변환 불가능한 값, 비유한값(inf), 범위 밖 수치는 valid=False입니다.
    """
    # TODO: 원본 Series는 변경하지 않습니다.
    raise NotImplementedError


if __name__ == "__main__":
    sample = pd.Series(["21.5", "", "68", "invalid"])
    print(temperature_status(sample).to_string(index=False))
