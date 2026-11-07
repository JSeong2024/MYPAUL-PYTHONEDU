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
    df=pd.DataFrame({'hour':[9,10,11,12],'score':[50,65,80,95]})
    return px.scatter(df,x='hour',y='score',color='score',color_continuous_scale='Viridis')


if __name__=="__main__":
    result=solve()
    print("Practice 16:",getattr(result,"__class__",type(result)).__name__)
