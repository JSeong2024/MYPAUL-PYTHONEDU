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
    df=pd.read_csv(DATA/'support_tickets.csv').head(120)
    return px.scatter(df,x='created_local',y='first_response_min',facet_col='team',facet_col_wrap=2)


if __name__=="__main__":
    result=solve()
    print("Practice 11:",getattr(result,"__class__",type(result)).__name__)
