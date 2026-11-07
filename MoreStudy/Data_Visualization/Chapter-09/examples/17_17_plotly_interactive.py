from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 확대·범례를 직접 조작할 수 있는 인터랙티브 결과
good,bad,daily,slots=weather_summary();import plotly.express as px
p=px.line(daily,x='date',y='temperature_c',color='region',title='Interactive Daily Mean Temperature')
html=ROOT/'figures'/'interactive'/'17_weather_plotly.html';html.parent.mkdir(parents=True,exist_ok=True)
p.write_html(str(html),include_plotlyjs=True,full_html=True)
fig,ax=plt.subplots(figsize=(9,4));
for region,g in daily.groupby('region'):ax.plot(g.date,g.temperature_c,label=region)
ax.set(title='Interactive Plotly — Static Reference',ylabel='Temperature (C)');ax.legend(ncol=4)
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"17_17_plotly_interactive.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
