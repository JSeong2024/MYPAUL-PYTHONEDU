from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 동일 입력·동일 기준은 같은 결과를 산출해야 함
good,bad,daily,slots,incidents=transit_summary();c=good.groupby('line').boardings.sum().sort_index()
fig,ax=plt.subplots(figsize=(8,4));ax.bar(c.index,c.values)
ax.set(title='Validated Transit Boardings',ylabel='Boardings (persons)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"15_15_report_reproducibility.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
