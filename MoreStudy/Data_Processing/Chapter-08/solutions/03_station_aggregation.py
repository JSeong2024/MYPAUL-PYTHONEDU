"""Exercise 03 — 관측소별 기온 평균 모범답안."""
import pandas as pd


def station_mean(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("station_id", as_index=False)
            .agg(avg_temperature_c=("temperature_c", "mean"))
            .sort_values("station_id").reset_index(drop=True)
            .assign(avg_temperature_c=lambda frame: frame["avg_temperature_c"].round(2)))


if __name__ == "__main__":
    data = pd.DataFrame({"station_id": ["ST-02", "ST-01", "ST-01"],
                         "temperature_c": [25.0, 20.0, 22.0]})
    print(station_mean(data).to_string(index=False))
