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

df=pd.read_csv(DATA/"retail_sales.csv")
table=df.pivot_table(index="store",columns="category",values="revenue_krw",aggfunc="sum",fill_value=0)
fig=px.imshow(table,text_auto=True,aspect="auto",color_continuous_scale="Blues",
              title="Sales Heatmap (KRW)")
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "16_heatmap.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 16:", len(fig.data), "traces; HTML generated")
