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

df=pd.read_csv(DATA/"support_tickets.csv")
fig=px.histogram(df,x="first_response_min",color="team",nbins=25,opacity=.72,
                 barmode="overlay",title="Response Time Histogram")
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "15_histogram.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 15:", len(fig.data), "traces; HTML generated")
