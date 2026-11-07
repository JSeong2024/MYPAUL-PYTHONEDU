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

fig = go.Figure()
fig.add_trace(go.Bar(x=["A", "B", "C"], y=[16, 23, 19], name="This Week"))
fig.add_trace(go.Bar(x=["A", "B", "C"], y=[14, 20, 22], name="Last Week"))
fig.update_layout(barmode="group", template="plotly_white", title="Two Weeks")

fig.write_html(OUT / "02_px_vs_go.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 02:", len(fig.data), "traces; HTML generated")
