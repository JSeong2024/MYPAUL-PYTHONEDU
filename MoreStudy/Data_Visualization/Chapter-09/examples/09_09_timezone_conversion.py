from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: UTC 날짜와 한국시간 날짜의 경계가 다를 수 있음
good,bad,daily=electricity_summary();g=good[good.region.eq('North')].head(48)
fig,ax=plt.subplots(figsize=(10,4));ax.plot(g.timestamp_kst,g.demand_mw)
ax.set(title='Hourly Demand (Asia/Seoul)',ylabel='Demand (MW)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"09_09_timezone_conversion.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
