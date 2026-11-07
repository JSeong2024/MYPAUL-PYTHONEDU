from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 관측 ID를 정류장 등 참조정보와 연결
good,bad,daily,slots=metro_summary()
c=good.groupby('line').boardings.sum();fig,ax=plt.subplots(figsize=(7,4));ax.bar(c.index,c.values)
ax.set(title='Boardings by Transit Line',ylabel='Validated boardings (persons)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"04_04_reference_join.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
