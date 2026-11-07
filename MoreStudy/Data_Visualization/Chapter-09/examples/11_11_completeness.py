from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 부분 기록의 일별 총량을 완전 관측일과 섞어 비교하지 않음
good,bad,daily,slots=metro_summary();counts=daily.groupby('complete').size().reindex([False,True],fill_value=0)
fig,ax=plt.subplots(figsize=(7,4));ax.bar(['Incomplete','Complete'],counts.values)
ax.set(title='Daily Station Coverage State',ylabel='Station-days (count)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"11_11_completeness.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
