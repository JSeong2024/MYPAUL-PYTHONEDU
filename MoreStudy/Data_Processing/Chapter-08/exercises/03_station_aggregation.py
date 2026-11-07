"""Exercise 03 — 관측소별 기온 평균을 구하세요."""
import pandas as pd


def station_mean(df: pd.DataFrame) -> pd.DataFrame:
    """station_id별 평균 온도를 계산하고 오름차순 정렬하여 반환하세요.

    반환 열: station_id, avg_temperature_c (소수 둘째 자리 반올림).
    """
    # TODO: 결측 temperature_c는 Pandas 평균 계산에서 제외됩니다.
    raise NotImplementedError


if __name__ == "__main__":
    data = pd.DataFrame({"station_id": ["ST-02", "ST-01", "ST-01"],
                         "temperature_c": [25.0, 20.0, 22.0]})
    print(station_mean(data).to_string(index=False))
