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
    # TODO: reindex 09:00–12:00 hourly and set connectgaps=False
    raise NotImplementedError


if __name__=="__main__":
    print(solve())
