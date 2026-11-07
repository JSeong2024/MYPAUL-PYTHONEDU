"""Public Bicycle Demand Report Generator — starter file.

TODO: Validate ride rows, link reporting slots, handle missing slots separately from zero, support selected stations and faceted report.
Reference implementation: solutions/ (do not read until after an attempt).
"""
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def run(output_dir=ROOT / "output" / "advanced_01_bike"):
    # TODO 1. Read and validate the necessary data.
    # TODO 2. Calculate statistics for the requested chart.
    # TODO 3. Draw Seaborn plots, then label and save the figures.
    # TODO 4. Check the output values and missing observations.
    raise NotImplementedError("Complete the project requirements in README.md")

if __name__ == "__main__":
    run()
