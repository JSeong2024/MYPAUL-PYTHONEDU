"""Starter — Challenge 02 — Electricity Load Audit. Finish the TODOs without opening the reference solution."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data'
OUTPUT = ROOT / 'output' / 'challenge_02_grid_incident'


def load_and_validate():
    # TODO 1: Read relevant CSV files and validate identifiers, timestamps and values.
    raise NotImplementedError


def summarize(valid_rows):
    # TODO 2: Return interpretable aggregations and missing-data indicators.
    raise NotImplementedError


def make_charts(summary):
    # TODO 3: Use Matplotlib/Seaborn and save clearly labelled PNG files.
    raise NotImplementedError


def main():
    # TODO 4: Connect the stages and save CSV/JSON results without changing source data.
    raise NotImplementedError


if __name__ == '__main__':
    main()
