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
    # TODO: scatter with color by score
    raise NotImplementedError


if __name__=="__main__":
    print(solve())
