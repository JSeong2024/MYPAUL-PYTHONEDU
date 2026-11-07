"""Solution 01 — weekly temperature line chart."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
TEMPERATURES = [20.0, 21.5, 19.0, 23.0, 22.5]


def draw_chart(output_path: Path) -> tuple[float, float]:
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.plot(DAYS, TEMPERATURES, marker="o")
    ax.set(title="Weekday Temperatures", xlabel="Day", ylabel="Temperature (°C)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return min(TEMPERATURES), max(TEMPERATURES)


if __name__ == "__main__":
    low, high = draw_chart(Path(__file__).resolve().parents[1] / "output" / "exercise01.png")
    print(f"Minimum: {low:.1f} °C")
    print(f"Maximum: {high:.1f} °C")
