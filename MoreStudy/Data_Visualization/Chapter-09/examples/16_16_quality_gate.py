from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 불완전한 날짜를 모른 채 일별 합계를 확정하지 않음
good,bad,daily,slots,incidents=transit_summary();p=slots.groupby('stop_id').available.mean()
fig,ax=plt.subplots(figsize=(8,4));ax.bar(p.index,p.values*100)
ax.set(title='Expected Slot Coverage',ylabel='Coverage (%)',ylim=(0,102))
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"16_16_quality_gate.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
