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
    df=pd.read_csv(DATA/'support_tickets.csv')
    return px.box(df,x='team',y='first_response_min',points='outliers')


if __name__=="__main__":
    result=solve()
    print("Practice 14:",getattr(result,"__class__",type(result)).__name__)
