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
    fig.update_xaxes(rangeselector=dict(buttons=[dict(count=7,label='7d',step='day',stepmode='backward'),dict(label='All',step='all')]))
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 07:",getattr(result,"__class__",type(result)).__name__)
