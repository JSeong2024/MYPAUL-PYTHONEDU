"""Solution 03 — temperature vs visits scatter plot."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def draw_chart(csv_path: Path, output_path: Path) -> int:
    frame = pd.read_csv(csv_path)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(frame["temperature_c"], frame["visitors"])
    ax.set(title="Temperature vs Park Visits", xlabel="Temperature (°C)", ylabel="Visitors (people/day)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return len(frame)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    count = draw_chart(root / "data" / "park_visits.csv", root / "output" / "exercise03.png")
    print("Points:", count)
