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

df=pd.read_csv(DATA/"retail_sales.csv").head(100)
fig=px.scatter(df,x="units",y="revenue_krw",color="category",size="unit_price_krw",
               hover_data=["store","date"],title="Sales: Quantity vs Revenue",size_max=25)
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "12_bubble_scatter.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 12:", len(fig.data), "traces; HTML generated")
