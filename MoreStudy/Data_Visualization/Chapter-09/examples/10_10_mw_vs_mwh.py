from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 전력 MW를 합계 내는 것이 자동으로 에너지 MWh가 되지는 않음
good,bad,daily=electricity_summary();summary=daily.groupby('region').mean_demand_mw.mean().sort_values()
fig,ax=plt.subplots(figsize=(8,4));ax.barh(summary.index,summary.values)
ax.set(title='Mean Power Demand by Region',xlabel='Power (MW)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"10_10_mw_vs_mwh.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
