from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 오류 행을 임의로 누락시키지 않고 사유를 표시
good,bad,daily,slots=weather_summary()
counts=bad['_reason'].value_counts();fig,ax=plt.subplots(figsize=(9,4));ax.barh(counts.index,counts.values)
ax.set(title='Excluded Rows by Reason',xlabel='Rows (count)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"03_03_quality_audit.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
