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
    fig=go.Figure(go.Scatter(x=[1,2,3,4],y=[5,8,6,9],mode='markers'))
    fig.update_layout(dragmode='select')
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 17:",getattr(result,"__class__",type(result)).__name__)
