from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 오류 건수보다 요청 대비 오류율이 중요한 경우
good,summary=latency_summary();fig,ax=plt.subplots(figsize=(7,4));ax.bar(summary.service,summary.error_rate*100)
ax.set(title='Service Error Rate',ylabel='Error rate (%)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"07_07_rates_denominators.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
