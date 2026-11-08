"""Chapter 01 교육용 가상 CSV를 결정적으로 생성합니다."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def make_weather() -> pd.DataFrame:
    rng = np.random.default_rng(1042)
    rain = rng.integers(5, 96, 100)
    wind = rng.integers(0, 36, 100)
    label = ((rain >= 58) | ((rain >= 38) & (wind <= 14))).astype(int)
    # 판단이 엇갈리는 사례를 섞어 데이터가 단순한 하나의 공식이 아니도록 구성합니다.
    label[[6, 22, 45, 77, 91]] = 1 - label[[6, 22, 45, 77, 91]]
    return pd.DataFrame({
        "case_id": [f"W{i:03d}" for i in range(1, 101)],
        "rain_probability_pct": rain,
        "wind_speed_kmh": wind,
        "umbrella_chosen": label,
    })


def make_rare_events() -> pd.DataFrame:
    rng = np.random.default_rng(2042)
    normal = rng.normal(loc=(0.0, 0.0), scale=(1.0, 1.0), size=(360, 2))
    rare = rng.normal(loc=(1.6, 1.5), scale=(1.0, 1.0), size=(40, 2))
    x = np.vstack((normal, rare))
    y = np.r_[np.zeros(360, dtype=int), np.ones(40, dtype=int)]
    order = rng.permutation(400)
    x, y = x[order], y[order]
    return pd.DataFrame({
        "record_id": [f"R{i:03d}" for i in range(1, 401)],
        "sensor_a": np.round(x[:, 0], 4),
        "sensor_b": np.round(x[:, 1], 4),
        "is_rare_event": y,
    })


def main() -> None:
    DATA.mkdir(exist_ok=True)
    make_weather().to_csv(DATA / "weather_choices.csv", index=False, encoding="utf-8")
    make_rare_events().to_csv(DATA / "rare_events.csv", index=False, encoding="utf-8")
    print("Created: data/weather_choices.csv, data/rare_events.csv")


if __name__ == "__main__":
    main()
