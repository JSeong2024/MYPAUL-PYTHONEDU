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
    fig=go.Figure(go.Scatter(x=[1,2,3],y=[3,2,4],mode='lines'))
    buttons=[dict(label='Lines',method='restyle',args=[{'mode':'lines'}]),dict(label='Points',method='restyle',args=[{'mode':'lines+markers'}])]
    fig.update_layout(updatemenus=[dict(buttons=buttons)])
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 09:",getattr(result,"__class__",type(result)).__name__)
