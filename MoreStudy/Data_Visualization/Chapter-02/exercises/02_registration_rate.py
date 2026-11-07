"""Exercise 02: Registration Rate. Implement the TODO and run this script."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "library_visits.csv"
OUTPUT = ROOT / "output" / "exercise_02.png"


def solve():
    frame = pd.read_csv(DATA, parse_dates=["date"])
    # TODO: Compute the total new_members / visitors percentage by branch; avoid averaging daily percentages.
    raise NotImplementedError("Complete this exercise")


if __name__ == "__main__":
    solve()
