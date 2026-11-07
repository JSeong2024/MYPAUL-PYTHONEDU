"""Solution 02 — category comparison."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALES = {"Books": 32, "Pens": 54, "Notebooks": 41, "Markers": 28}


def draw_chart(output_path: Path) -> int:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(list(SALES), list(SALES.values()))
    ax.set(title="Shop Sales by Category", xlabel="Product", ylabel="Units sold")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return sum(SALES.values())


if __name__ == "__main__":
    total = draw_chart(Path(__file__).resolve().parents[1] / "output" / "exercise02.png")
    print("Total units:", total)
