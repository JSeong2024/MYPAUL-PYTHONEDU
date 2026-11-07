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

fig=go.Figure(go.Scatter(x=["A","B","C"],y=[5,8,7],mode="lines+markers"))
fig.update_layout(title="Figure JSON",template="plotly_white")
fig.write_json(ROOT / "figures/interactive/21_figure.json")
restored=__import__("plotly.io", fromlist=["from_json"]).from_json(fig.to_json())
assert len(restored.data)==1

fig.write_html(OUT / "21_figure_json.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 21:", len(fig.data), "traces; HTML generated")
