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
fig=px.box(df,x="team",y="first_response_min",color="team",points="outliers",
           title="Response Time by Team")
fig.update_layout(template="plotly_white",showlegend=False)

fig.write_html(OUT / "14_boxplot.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 14:", len(fig.data), "traces; HTML generated")
