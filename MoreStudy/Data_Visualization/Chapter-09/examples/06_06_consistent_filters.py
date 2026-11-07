from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: KPI와 그래프에 동일한 데이터 필터를 적용
good,daily=retail_summary();part=daily[daily.store_id.eq('S-01')]
fig,ax=plt.subplots(figsize=(9,4));ax.plot(pd.to_datetime(part.date),part.revenue_krw)
ax.set(title=f'Store S-01 Revenue — Total {int(part.revenue_krw.sum()):,} KRW',ylabel='Revenue (KRW)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"06_06_consistent_filters.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
