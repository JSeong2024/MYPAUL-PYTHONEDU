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
summary=df.groupby("store",as_index=False).agg(total_revenue=("revenue_krw","sum"))
fig=px.bar(summary,x="store",y="total_revenue",text_auto=True,
           title="Store Total Revenue",labels={"total_revenue":"Revenue (KRW)"})
fig.update_layout(template="plotly_white",yaxis_rangemode="tozero")

fig.write_html(OUT / "13_bar_aggregation.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 13:", len(fig.data), "traces; HTML generated")
