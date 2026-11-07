"""City Weather Snapshot: 교육용 가상 기상 데이터의 시각화 보고서."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA_FILE = ROOT / "data" / "weather_daily.csv"
OUTPUT_DIR = ROOT / "output"
REGIONS = ["Seoul", "Busan", "Gwangju"]


def load_weather(path: Path = DATA_FILE) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["date"])
    required = {"date", "region", "temperature_c", "precipitation_mm"}
    if not required.issubset(data.columns):
        raise ValueError("Required columns are missing")
    if data.duplicated(["date", "region"]).any():
        raise ValueError("Duplicate date-region observations")
    if not set(data["region"]).issubset(REGIONS):
        raise ValueError("Unknown region")
    if (data["precipitation_mm"].dropna() < 0).any():
        raise ValueError("Precipitation cannot be negative")
    return data


def summarize(data: pd.DataFrame) -> dict:
    first, last = data["date"].min(), data["date"].max()
    expected_dates = pd.date_range(first, last, freq="D")
    expected = len(expected_dates) * len(REGIONS)
    count_valid_temp = int(data["temperature_c"].notna().sum())
    return {
        "expected_rows": expected,
        "observed_rows": len(data),
        "temperature_valid_rows": count_valid_temp,
        "missing_rows": expected - len(data),
        "missing_temperature_cells": int(data["temperature_c"].isna().sum()),
        "total_precipitation_mm": round(float(data["precipitation_mm"].sum()), 1),
    }


def build_figure(data: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    dates = pd.date_range(data["date"].min(), data["date"].max(), freq="D")
    ax = axes[0, 0]
    for region in REGIONS:
        series = (data.loc[data["region"] == region]
                  .set_index("date")["temperature_c"].reindex(dates))
        ax.plot(dates, series, marker="o", markersize=3, label=region)
    ax.set(title="Daily Mean Temperature", ylabel="Temperature (°C)")
    ax.legend(ncol=3, fontsize=9)
    ax.tick_params(axis="x", labelrotation=30)
    ax.grid(alpha=0.2)

    ax = axes[0, 1]
    rain = data.groupby("region")["precipitation_mm"].sum().reindex(REGIONS)
    bars = ax.bar(rain.index, rain.values)
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set(title="Total Rainfall", ylabel="Precipitation (mm)")
    ax.set_ylim(0, max(rain) * 1.3)

    ax = axes[1, 0]
    for region in REGIONS:
        part = data.loc[data["region"] == region]
        ax.scatter(part["temperature_c"], part["precipitation_mm"],
                   s=35, alpha=0.65, label=region)
    ax.set(title="Temperature and Rainfall", xlabel="Temperature (°C)",
           ylabel="Precipitation (mm)")
    ax.legend(ncol=3, fontsize=9)

    ax = axes[1, 1]
    by_day = data.groupby("date").size().reindex(dates, fill_value=0)
    ax.plot(dates, by_day, marker="o", label="Observed")
    ax.axhline(len(REGIONS), linestyle="--", label="Expected")
    ax.set(title="Daily Data Coverage", ylabel="Recorded regions", ylim=(0, 3.4))
    ax.tick_params(axis="x", labelrotation=30)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.2)

    fig.suptitle("City Weather Snapshot — Synthetic Data", fontsize=15)
    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_weather()
    summary = summarize(data)
    figure = build_figure(data)
    figure.savefig(OUTPUT_DIR / "weather_dashboard.png", dpi=150)
    # README sample image is generated separately during packaging.
    plt.close(figure)
    (OUTPUT_DIR / "weather_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
