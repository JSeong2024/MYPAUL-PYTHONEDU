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

df=pd.read_csv(DATA/"support_tickets.csv").head(240)
df["ticket_index"]=np.arange(len(df))
fig=px.scatter(df,x="ticket_index",y="first_response_min",color="team",hover_name="ticket_id",
               title="Use Box Select or Lasso Select")
fig.update_layout(dragmode="select",template="plotly_white")

fig.write_html(OUT / "18_selection.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 18:", len(fig.data), "traces; HTML generated")
