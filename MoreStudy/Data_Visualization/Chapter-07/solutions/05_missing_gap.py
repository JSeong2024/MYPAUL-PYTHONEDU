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
    observed=pd.Series([10,0,18],index=pd.to_datetime(['2026-10-01 09:00','2026-10-01 10:00','2026-10-01 12:00']))
    times=pd.date_range('2026-10-01 09:00',periods=4,freq='h')
    filled=observed.reindex(times)
    return go.Figure(go.Scatter(x=filled.index,y=filled,connectgaps=False,mode='lines+markers'))


if __name__=="__main__":
    result=solve()
    print("Practice 05:",getattr(result,"__class__",type(result)).__name__)
