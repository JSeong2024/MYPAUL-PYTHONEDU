from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 개별 기록과 일별 평균은 서로 다른 단위
good,bad,daily,slots=weather_summary(); sample=good[good.station_id.eq('ST-01')]
fig,ax=plt.subplots(figsize=(10,4));ax.scatter(sample['_parsed'],sample.temperature_c,s=14,label='Observations')
part=daily[daily.station_id.eq('ST-01')];ax.plot(part.date,part.temperature_c,label='Daily mean')
ax.set(title='Observation vs Daily Aggregate',ylabel='Temperature (C)');ax.legend()
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"02_02_grain_vs_aggregation.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
