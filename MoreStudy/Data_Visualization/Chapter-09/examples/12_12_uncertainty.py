from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 표본수가 적은 집계 결과는 신뢰도가 떨어질 수 있음
good,summary=latency_summary();fig,ax=plt.subplots(figsize=(8,4));ax.bar(summary.service,summary.median_ms,label='Median')
ax.scatter(summary.service,summary.p95_ms,color='black',zorder=3,label='P95')
ax.set(title='Median vs P95 Latency',ylabel='Latency (ms)');ax.legend()
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"12_12_uncertainty.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
