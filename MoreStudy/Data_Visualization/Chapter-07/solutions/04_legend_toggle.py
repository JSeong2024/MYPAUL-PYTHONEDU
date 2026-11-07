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
    fig.add_trace(go.Scatter(x=hours,y=[120,150,130],mode='lines',name='API-A'))
    fig.add_trace(go.Scatter(x=hours,y=[180,170,190],mode='lines',name='API-B'))
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 04:",getattr(result,"__class__",type(result)).__name__)
