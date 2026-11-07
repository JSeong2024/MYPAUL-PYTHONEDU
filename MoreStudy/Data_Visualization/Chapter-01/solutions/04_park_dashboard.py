"""Solution 04 — a small two-panel park dashboard."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def build_dashboard(csv_path: Path, output_path: Path) -> dict:
    frame = pd.read_csv(csv_path, parse_dates=["date"]).sort_values("date")
    rainy = frame["rainfall_mm"].gt(0)
    means = [frame.loc[~rainy, "visitors"].mean(), frame.loc[rainy, "visitors"].mean()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(frame["date"], frame["visitors"], marker="o")
    ax1.set(title="Daily Visits", xlabel="Date", ylabel="Visitors (people/day)")
    ax1.grid(axis="y", alpha=0.25)
    ax2.bar(["Dry", "Rainy"], means)
    ax2.set(title="Mean Visits by Rain Status", xlabel="Day type", ylabel="Visitors (people/day)")
    ax2.set_ylim(bottom=0)
    fig.autofmt_xdate(); fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return {"total_visitors": int(frame["visitors"].sum()), "rainy_days": int(rainy.sum())}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print(build_dashboard(root / "data" / "park_visits.csv", root / "output" / "exercise04.png"))
