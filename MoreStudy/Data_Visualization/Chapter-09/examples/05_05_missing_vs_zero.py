from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 실제로 기록되지 않은 관측 슬롯은 측정값 0이 아님
good,bad,daily,slots=weather_summary();sub=slots[slots.station_id.eq('ST-02')]
c=sub.groupby('date').available.sum();fig,ax=plt.subplots(figsize=(10,4));ax.plot(c.index,c.values,marker='o')
ax.set(title='Daily Observation Coverage',ylabel='Valid records (0–2)',ylim=(-.1,2.3))
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"05_05_missing_vs_zero.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
