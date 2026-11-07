"""Exercise 04: Compare Two Encodings. Implement the TODO and run this script."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "library_visits.csv"
OUTPUT = ROOT / "output" / "exercise_04.png"


def solve():
    frame = pd.read_csv(DATA, parse_dates=["date"])
    # TODO: Represent scores 80 and 85 with a zero-based bar chart and a close-range dot plot side by side.
    raise NotImplementedError("Complete this exercise")


if __name__ == "__main__":
    solve()
