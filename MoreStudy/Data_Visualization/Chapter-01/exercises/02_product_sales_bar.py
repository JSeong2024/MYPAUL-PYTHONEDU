"""Exercise 02 — category comparison with a bar chart."""
from pathlib import Path

SALES = {"Books": 32, "Pens": 54, "Notebooks": 41, "Markers": 28}


def draw_chart(output_path: Path) -> int:
    """Save a bar chart with a zero-based y-axis; return total sales units."""
    # TODO: Draw and save the bar chart.
    raise NotImplementedError


if __name__ == "__main__":
    draw_chart(Path(__file__).resolve().parents[1] / "output" / "exercise02.png")
