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

fig=go.Figure(go.Bar(x=["Mon","Tue","Wed"],y=[18,22,25],name="Tickets"))
fig.update_layout(template="plotly_white",title="Offline HTML Example")
fig.write_html(ROOT / "figures/interactive/20_single_file.html", include_plotlyjs=True)

fig.write_html(OUT / "20_html_offline.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 20:", len(fig.data), "traces; HTML generated")
