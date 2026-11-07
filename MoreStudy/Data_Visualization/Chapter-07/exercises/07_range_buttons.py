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
    fig=go.Figure(go.Scatter(x=pd.date_range('2026-10-01',periods=20),y=list(range(20))))
    # TODO: add a 7d and All rangeselector
    return fig


if __name__=="__main__":
    print(solve())
