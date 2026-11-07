"""Exercise 01 — create a weekly line chart."""
from pathlib import Path

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
TEMPERATURES = [20.0, 21.5, 19.0, 23.0, 22.5]


def draw_chart(output_path: Path) -> tuple[float, float]:
    """Save PNG with day/temperature labels, then return (min, max)."""
    # TODO: Use Matplotlib to draw the line graph and save the image.
    raise NotImplementedError


if __name__ == "__main__":
    draw_chart(Path(__file__).resolve().parents[1] / "output" / "exercise01.png")
