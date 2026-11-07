from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figures" / "interactive"
OUT.mkdir(parents=True, exist_ok=True)

fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[11, 18, 16, 24], mode="lines", name="Orders"))
fig.update_layout(updatemenus=[dict(type="buttons", buttons=[
    dict(label="Lines", method="restyle", args=[{"mode": "lines"}]),
    dict(label="Lines + Markers", method="restyle", args=[{"mode": "lines+markers"}]),
],x=.5,xanchor="center",y=1.22)],margin=dict(t=95),template="plotly_white",title="Trace Style")

fig.write_html(OUT / "09_buttons_update.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 09:", len(fig.data), "traces; HTML generated")
