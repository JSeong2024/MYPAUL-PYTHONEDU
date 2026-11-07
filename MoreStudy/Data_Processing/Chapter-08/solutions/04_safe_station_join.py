"""Exercise 04 — 안전한 참조 테이블 결합 모범답안."""
import pandas as pd


def join_station_region(observations: pd.DataFrame, stations: pd.DataFrame) -> pd.DataFrame:
    if stations["station_id"].duplicated().any():
        raise ValueError("Duplicate station_id in reference data")
    merged = observations.merge(stations[["station_id", "region"]], on="station_id",
                                how="left", validate="many_to_one", indicator=True, sort=False)
    if not merged["_merge"].eq("both").all():
        raise ValueError("Unknown station_id")
    return merged[["station_id", "region"]]


if __name__ == "__main__":
    observations = pd.DataFrame({"station_id": ["ST-02", "ST-01"]})
    stations = pd.DataFrame({"station_id": ["ST-01", "ST-02"], "region": ["Seoul", "Busan"]})
    print(join_station_region(observations, stations).to_string(index=False))
