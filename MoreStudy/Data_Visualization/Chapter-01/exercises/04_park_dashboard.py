"""Exercise 04 — two views of a single CSV dataset."""
from pathlib import Path


def build_dashboard(csv_path: Path, output_path: Path) -> dict:
    """Save a 1x2 figure (line + bar); return visitors total and rainy-day count."""
    # TODO: Validate/read data, build two labelled subplots, save, return summary.
    raise NotImplementedError


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    build_dashboard(root / "data" / "park_visits.csv", root / "output" / "exercise04.png")
