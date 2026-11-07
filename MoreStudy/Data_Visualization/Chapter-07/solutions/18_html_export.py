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
    fig=go.Figure(go.Bar(x=['A','B'],y=[3,7]))
    output=ROOT/'output/practice_18.html'
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.write_html(output,include_plotlyjs=True)
    return output


if __name__=="__main__":
    result=solve()
    print("Practice 18:",getattr(result,"__class__",type(result)).__name__)
