"""Exercise 01 — DataFrame의 필수 열 존재 여부를 검사하세요."""
import pandas as pd


def check_required_columns(df: pd.DataFrame, columns: list[str]) -> bool:
    """columns에 명시된 열이 모두 있으면 True를 반환하세요."""
    # TODO: 빈 columns 목록은 True입니다.
    raise NotImplementedError


if __name__ == "__main__":
    sample = pd.DataFrame({"station_id": ["ST-01"], "temperature_c": [21.0]})
    print(check_required_columns(sample, ["station_id", "temperature_c"]))
