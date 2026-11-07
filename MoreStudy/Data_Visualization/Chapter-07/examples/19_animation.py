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

df=pd.read_csv(DATA/"support_tickets.csv",parse_dates=["created_local"])
df["week"]=df.created_local.dt.to_period("W").astype(str)
grouped=df.groupby(["week","team"],as_index=False).first_response_min.mean()
fig=px.bar(grouped,x="team",y="first_response_min",animation_frame="week",
           range_y=[0,float(grouped.first_response_min.max())*1.2],
           title="Weekly Response Time (Mean)",labels={"first_response_min":"Mean Response (min)"})
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "19_animation.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 19:", len(fig.data), "traces; HTML generated")
