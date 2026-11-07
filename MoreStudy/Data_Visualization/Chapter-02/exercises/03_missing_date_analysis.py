"""Exercise 03: Missing Date Analysis. Implement the TODO and run this script."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "library_visits.csv"
OUTPUT = ROOT / "output" / "exercise_03.png"


def solve():
    frame = pd.read_csv(DATA, parse_dates=["date"])
    # TODO: Build the full branch/date grid; keep absent observations as NaN and mark missing days.
    raise NotImplementedError("Complete this exercise")


if __name__ == "__main__":
    solve()
