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

df=pd.DataFrame({"station":["A","B","C","D","E"],"hour":[8,9,10,11,12],"score":[55,64,71,86,94]})
fig=px.scatter(df,x="hour",y="score",color="score",text="station",
               color_continuous_scale="Viridis",title="Continuous Score Color")
fig.update_traces(textposition="top center",marker_size=15)
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "17_color_types.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 17:", len(fig.data), "traces; HTML generated")
