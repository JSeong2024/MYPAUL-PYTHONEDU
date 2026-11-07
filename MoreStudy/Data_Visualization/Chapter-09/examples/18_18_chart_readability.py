from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 축·단위·라벨·폰트 등 기본 가독성을 점검
good,daily=retail_summary();g=daily.groupby('store_id').revenue_krw.sum().sort_values()
fig,ax=plt.subplots(figsize=(9,4));bars=ax.barh(g.index,g.values)
ax.bar_label(bars,padding=4,fmt='%.0f');ax.set(title='Completed Sales by Store',xlabel='Revenue (KRW)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"18_18_chart_readability.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
