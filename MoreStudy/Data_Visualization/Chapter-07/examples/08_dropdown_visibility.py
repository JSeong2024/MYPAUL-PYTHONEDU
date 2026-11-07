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
daily = df.groupby(["date", "store"], as_index=False)["revenue_krw"].sum()
stores = sorted(daily.store.unique())
fig = go.Figure()
for store in stores:
    one = daily[daily.store == store]
    fig.add_trace(go.Scatter(x=one.date, y=one.revenue_krw, name=store, mode="lines"))
buttons = [dict(label="All", method="update", args=[{"visible": [True] * len(stores)}])]
for i, store in enumerate(stores):
    buttons.append(dict(label=store, method="update", args=[{"visible": [j == i for j in range(len(stores))]}]))
fig.update_layout(updatemenus=[dict(buttons=buttons, x=1, y=1.22, xanchor="right")],
                  margin=dict(t=110), template="plotly_white", title="Choose Store")

fig.write_html(OUT / "08_dropdown_visibility.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 08:", len(fig.data), "traces; HTML generated")
