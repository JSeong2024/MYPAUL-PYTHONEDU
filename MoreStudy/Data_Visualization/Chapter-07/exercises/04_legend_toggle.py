"""Partial-code exercise. Fill the TODO lines, then run the file."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def solve():
    fig=go.Figure()
    hours=['09:00','10:00','11:00']
    # TODO: add two named line traces for API-A [120,150,130], API-B [180,170,190]
    return fig


if __name__=="__main__":
    print(solve())
