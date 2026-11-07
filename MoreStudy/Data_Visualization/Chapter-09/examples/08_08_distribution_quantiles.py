from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 평균만으로는 응답 지연의 긴 꼬리를 파악하기 어려움
good,summary=latency_summary();fig,ax=plt.subplots(figsize=(9,4));ax.boxplot([g.latency_ms for _,g in good.groupby('service')],tick_labels=list(good.groupby('service').groups),showfliers=False)
ax.set(title='Latency Distribution by Service',ylabel='Latency (ms)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"08_08_distribution_quantiles.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
