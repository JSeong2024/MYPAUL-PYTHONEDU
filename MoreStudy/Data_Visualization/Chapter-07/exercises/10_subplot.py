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
    fig=make_subplots(rows=1,cols=2)
    # TODO: left bar [10,20]; right scatter [80,90]
    return fig


if __name__=="__main__":
    print(solve())
