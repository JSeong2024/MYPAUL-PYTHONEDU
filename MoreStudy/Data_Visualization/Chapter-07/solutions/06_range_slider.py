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
    df=pd.read_csv(DATA/'retail_sales.csv',parse_dates=['date'])
    daily=df.groupby('date',as_index=False).revenue_krw.sum()
    fig=px.line(daily,x='date',y='revenue_krw')
    fig.update_xaxes(rangeslider_visible=True)
    return fig


if __name__=="__main__":
    result=solve()
    print("Practice 06:",getattr(result,"__class__",type(result)).__name__)
