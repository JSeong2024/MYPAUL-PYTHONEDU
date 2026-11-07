"""Exercise 05: Small Multiples. Implement the TODO and run this script."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "library_visits.csv"
OUTPUT = ROOT / "output" / "exercise_05.png"


def solve():
    frame = pd.read_csv(DATA, parse_dates=["date"])
    # TODO: Draw four subplots with one shared y-axis range and preserve missing Eastgate observations.
    raise NotImplementedError("Complete this exercise")


if __name__ == "__main__":
    solve()
