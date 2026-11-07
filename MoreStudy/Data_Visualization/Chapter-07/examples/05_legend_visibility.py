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

df = pd.read_csv(DATA / "retail_sales.csv", parse_dates=["date"])
daily = df.groupby(["date", "store"], as_index=False)["revenue_krw"].sum()
fig = px.line(daily, x="date", y="revenue_krw", color="store",
              title="Toggle Store Lines")
fig.update_layout(template="plotly_white", hovermode="x unified")

fig.write_html(OUT / "05_legend_visibility.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 05:", len(fig.data), "traces; HTML generated")
