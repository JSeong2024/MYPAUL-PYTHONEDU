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

df = pd.read_csv(DATA / "retail_sales.csv").head(40)
fig = px.scatter(df, x="units", y="revenue_krw", color="category",
                 hover_name="store", hover_data=["date", "unit_price_krw"],
                 title="Sales Detail on Hover")
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "03_hover_data.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 03:", len(fig.data), "traces; HTML generated")
