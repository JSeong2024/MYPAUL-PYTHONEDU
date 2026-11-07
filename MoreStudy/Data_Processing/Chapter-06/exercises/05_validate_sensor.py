"""Exercise 05. 센서 날짜와 온도의 유효성을 검사한 뒤 유효한 행만 반환하세요."""
import pandas as pd


def valid_sensor_rows(frame: pd.DataFrame) -> pd.DataFrame:
    # TODO: date=YYYY-MM-DD, temperature_c=-40~85 유한한 수만 허용합니다.
    # 결과는 date(datetime64)와 temperature_c(float)가 있는 새 DataFrame입니다.
    raise NotImplementedError


if __name__ == "__main__":
    demo = pd.DataFrame({
        "date": ["2026-10-01", "2026-02-30", "2026-10-03"],
        "temperature_c": ["23.5", "20", "999"],
    })
    print(valid_sensor_rows(demo))
