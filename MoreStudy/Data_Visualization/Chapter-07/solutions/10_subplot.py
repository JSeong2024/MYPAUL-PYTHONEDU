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
    fig.add_trace(go.Bar(x=['Jan','Feb'],y=[10,20]),row=1,col=1)
    fig.add_trace(go.Scatter(x=['Jan','Feb'],y=[80,90],mode='lines'),row=1,col=2)
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 10:",getattr(result,"__class__",type(result)).__name__)
