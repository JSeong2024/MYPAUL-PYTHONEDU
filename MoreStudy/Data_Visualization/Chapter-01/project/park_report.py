"""City Park Visitor Snapshot — educational synthetic data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REQUIRED = {"date", "temperature_c", "rainfall_mm", "visitors"}


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load the supplied one-record-per-day dataset and check basic constraints."""
    frame = pd.read_csv(csv_path)
    if not REQUIRED.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(REQUIRED - set(frame.columns))}")
    if frame.empty:
        raise ValueError("No data rows")
    frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="coerce")
    if frame["date"].isna().any() or frame["date"].duplicated().any():
        raise ValueError("Invalid or duplicate dates")
    for col in ("temperature_c", "rainfall_mm", "visitors"):
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
        if frame[col].isna().any() or not np.isfinite(frame[col].to_numpy(dtype=float)).all():
            raise ValueError(f"Invalid numeric values: {col}")
    if not frame["temperature_c"].between(-30, 45).all():
        raise ValueError("Temperature outside exercise policy")
    if (frame["rainfall_mm"] < 0).any() or (frame["visitors"] < 0).any():
        raise ValueError("Negative rainfall or visitors")
    if not (frame["visitors"] % 1 == 0).all():
        raise ValueError("Visitor counts must be integers")
    return frame.sort_values("date").reset_index(drop=True)


def summarize(frame: pd.DataFrame) -> dict:
    is_rainy = frame["rainfall_mm"].gt(0)
    dry_mean = frame.loc[~is_rainy, "visitors"].mean()
    rainy_mean = frame.loc[is_rainy, "visitors"].mean()
    return {
        "days": int(len(frame)),
        "total_visitors": int(frame["visitors"].sum()),
        "mean_daily_visitors": round(float(frame["visitors"].mean()), 2),
        "rainy_days": int(is_rainy.sum()),
        "dry_days": int((~is_rainy).sum()),
        "mean_visitors_rainy": None if pd.isna(rainy_mean) else round(float(rainy_mean), 2),
        "mean_visitors_dry": None if pd.isna(dry_mean) else round(float(dry_mean), 2),
        "dataset": "Synthetic training data",
    }


def make_charts(frame: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(frame["date"], frame["visitors"], marker="o")
    ax.set(title="Daily Park Visits", xlabel="Date", ylabel="Visitors (people/day)")
    ax.grid(axis="y", alpha=0.3)
    fig.autofmt_xdate(); fig.tight_layout()
    fig.savefig(output_dir / "visitor_trend.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    rainy = frame["rainfall_mm"].gt(0)
    labels = ["Dry", "Rainy"]
    means = [frame.loc[~rainy, "visitors"].mean(), frame.loc[rainy, "visitors"].mean()]
    ax.bar(labels, means)
    ax.set(title="Average Visits by Rain Status", xlabel="Day type", ylabel="Mean visitors (people/day)")
    ax.set_ylim(bottom=0); ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "rain_status_comparison.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(frame["temperature_c"], frame["visitors"])
    ax.set(title="Temperature and Visits", xlabel="Temperature (°C)", ylabel="Visitors (people/day)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "temperature_scatter.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(frame["visitors"], bins=[80, 120, 160, 200, 240, 280], edgecolor="white")
    ax.set(title="Distribution of Daily Visits", xlabel="Visitors (people/day)", ylabel="Number of days")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "visitor_histogram.png", dpi=150); plt.close(fig)


def run_report(csv_path: Path, output_dir: Path) -> dict:
    frame = load_data(csv_path)
    result = summarize(frame)
    make_charts(frame, output_dir)
    (output_dir / "summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    chapter_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Generate a synthetic park visitor report")
    parser.add_argument("--input", type=Path, default=chapter_root / "data" / "park_visits.csv")
    parser.add_argument("--output", type=Path, default=chapter_root / "output" / "park_report")
    args = parser.parse_args()
    report = run_report(args.input, args.output)
    print(f"Days: {report['days']}")
    print(f"Total visitors: {report['total_visitors']}")
    print(f"Rainy days: {report['rainy_days']}")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()
