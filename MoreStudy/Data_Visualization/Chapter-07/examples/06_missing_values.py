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

source = pd.DataFrame({"time": pd.to_datetime(["2026-10-01 09:00", "2026-10-01 10:00", "2026-10-01 12:00"]),
                       "count": [8, 0, 13]}).set_index("time")
expected = pd.date_range("2026-10-01 09:00", periods=4, freq="h")
full = source.reindex(expected)
fig = go.Figure(go.Scatter(x=full.index, y=full["count"], mode="lines+markers", connectgaps=False))
fig.update_layout(title="11:00 is Missing; 10:00 Is Zero", template="plotly_white")

fig.write_html(OUT / "06_missing_values.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 06:", len(fig.data), "traces; HTML generated")
