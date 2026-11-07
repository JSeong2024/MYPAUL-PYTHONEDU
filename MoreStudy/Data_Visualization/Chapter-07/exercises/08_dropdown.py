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
    for name,values in [('A',[5,8]),('B',[7,6]),('C',[9,10])]:
        fig.add_trace(go.Scatter(x=[1,2],y=values,name=name))
    # TODO: one button per trace with matching visible array
    return fig


if __name__=="__main__":
    print(solve())
