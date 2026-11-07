"""Exercise 04 — 관측값에 관측소 지역 정보를 결합하세요."""
import pandas as pd


def join_station_region(observations: pd.DataFrame, stations: pd.DataFrame) -> pd.DataFrame:
    """station_id 기준 many-to-one 결합 후 station_id·region 열을 반환하세요.

    미등록 관측소나 기준정보에 중복 station_id가 있으면 ValueError를 발생시킵니다.
    입력 observations의 행 순서를 유지하세요.
    """
    # TODO: merge(validate=...)와 indicator=...를 사용합니다.
    raise NotImplementedError


if __name__ == "__main__":
    observations = pd.DataFrame({"station_id": ["ST-02", "ST-01"]})
    stations = pd.DataFrame({"station_id": ["ST-01", "ST-02"], "region": ["Seoul", "Busan"]})
    print(join_station_region(observations, stations).to_string(index=False))
