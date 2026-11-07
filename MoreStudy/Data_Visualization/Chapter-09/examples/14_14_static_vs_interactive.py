from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: PNG는 공유에 유리하고 Plotly HTML은 필터·확대가 가능
good,bad,daily,slots=weather_summary();s=daily[daily.station_id.eq('ST-02')]
fig,ax=plt.subplots(figsize=(9,4));ax.plot(s.date,s.temperature_c,marker='o')
ax.set(title='Static PNG Weather Overview',ylabel='Temperature (C)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"14_14_static_vs_interactive.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
