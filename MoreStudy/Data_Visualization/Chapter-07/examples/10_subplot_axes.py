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

fig = make_subplots(rows=1, cols=2, subplot_titles=("Visitors", "Revenue (10k KRW)"))
fig.add_trace(go.Bar(x=["Jan","Feb","Mar"],y=[110,150,130],name="Visitors"),row=1,col=1)
fig.add_trace(go.Scatter(x=["Jan","Feb","Mar"],y=[81,102,96],mode="lines+markers",name="Revenue"),row=1,col=2)
fig.update_layout(template="plotly_white",title="Two Units, Two Panels")

fig.write_html(OUT / "10_subplot_axes.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 10:", len(fig.data), "traces; HTML generated")
