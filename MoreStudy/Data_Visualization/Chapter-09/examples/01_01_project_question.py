from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 날짜별 방문 또는 관측 기록을 어떤 단위로 집계해야 하는지 확인
good,bad,daily,slots=weather_summary()
summary=daily.groupby('region').temperature_c.mean().sort_values()
fig,ax=plt.subplots(figsize=(8,4));ax.barh(summary.index,summary.values)
ax.set(title='Average Temperature by Region',xlabel='Mean temperature (C)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"01_01_project_question.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
