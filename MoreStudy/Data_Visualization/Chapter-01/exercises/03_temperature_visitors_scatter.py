"""Exercise 03 — temperature vs visits scatter plot."""
from pathlib import Path


def draw_chart(csv_path: Path, output_path: Path) -> int:
    """Save a scatter plot from CSV and return number of points."""
    # TODO: Read temperature_c and visitors with pandas, then scatter plot.
    raise NotImplementedError


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    draw_chart(root / "data" / "park_visits.csv", root / "output" / "exercise03.png")
