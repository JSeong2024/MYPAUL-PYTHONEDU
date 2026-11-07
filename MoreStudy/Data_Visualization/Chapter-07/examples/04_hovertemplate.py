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

df = pd.read_csv(DATA / "retail_sales.csv").head(30)
fig = px.scatter(df, x="units", y="revenue_krw", color="store",
                 custom_data=["date", "category"])
fig.update_traces(hovertemplate="Units: %{x}<br>Revenue: %{y:,.0f} KRW<br>Date: %{customdata[0]}<br>Category: %{customdata[1]}<extra></extra>")
fig.update_layout(template="plotly_white", title="Formatted Hover")

fig.write_html(OUT / "04_hovertemplate.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 04:", len(fig.data), "traces; HTML generated")
