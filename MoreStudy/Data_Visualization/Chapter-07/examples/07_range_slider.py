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
daily = df.groupby("date", as_index=False)["revenue_krw"].sum()
fig = px.line(daily, x="date", y="revenue_krw", title="Sales — Select Date Range")
fig.update_xaxes(rangeslider_visible=True,
                 rangeselector=dict(buttons=[dict(count=7, label="7d", step="day", stepmode="backward"),
                                             dict(count=1, label="1m", step="month", stepmode="backward"),
                                             dict(label="All", step="all")]))
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "07_range_slider.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 07:", len(fig.data), "traces; HTML generated")
