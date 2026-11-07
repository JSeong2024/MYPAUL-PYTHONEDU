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
    buttons=[dict(label=fig.data[i].name,method='update',args=[{'visible':[j==i for j in range(3)]}]) for i in range(3)]
    fig.update_layout(updatemenus=[dict(buttons=buttons)])
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 08:",getattr(result,"__class__",type(result)).__name__)
