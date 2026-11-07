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

rng=np.random.default_rng(51)
n=4000
data=pd.DataFrame({"x":rng.normal(size=n),"y":rng.normal(size=n)})
fig=px.scatter(data,x="x",y="y",render_mode="webgl",
               title="4000 Points with Scattergl")
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "22_scattergl_performance.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 22:", len(fig.data), "traces; HTML generated")
