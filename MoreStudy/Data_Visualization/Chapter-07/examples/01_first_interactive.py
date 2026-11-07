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

frame = pd.DataFrame({"day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                      "revenue": [82000, 91000, 86000, 104000, 117000]})
fig = px.line(frame, x="day", y="revenue", markers=True,
              title="Weekday Revenue", labels={"revenue": "Revenue (KRW)"})
fig.update_layout(template="plotly_white")

fig.write_html(OUT / "01_first_interactive.html", include_plotlyjs="directory", config={"displaylogo": False, "responsive": True})
print("Example 01:", len(fig.data), "traces; HTML generated")
