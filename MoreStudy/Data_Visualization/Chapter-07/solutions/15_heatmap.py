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
    df=pd.read_csv(DATA/'retail_sales.csv')
    table=df.pivot_table(index='store',columns='category',values='revenue_krw',aggfunc='sum',fill_value=0)
    return px.imshow(table,text_auto=True,aspect='auto')


if __name__=="__main__":
    result=solve()
    print("Practice 15:",getattr(result,"__class__",type(result)).__name__)
