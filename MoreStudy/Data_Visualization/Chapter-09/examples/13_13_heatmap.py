from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

# 문제 상황: 서로 다른 정류장의 시간별 이용 분포 확인
good,bad,daily,slots,incidents=transit_summary();heat=good.assign(hour=good['_parsed'].dt.hour).pivot_table(index='stop_id',columns='hour',values='boardings',aggfunc='mean')
fig,ax=plt.subplots(figsize=(11,5));im=ax.imshow(heat.to_numpy(),aspect='auto')
ax.set(title='Mean Boardings by Stop and Hour',yticks=range(len(heat.index)),yticklabels=heat.index,xticks=range(len(heat.columns)),xticklabels=heat.columns)
fig.colorbar(im,ax=ax,label='Mean boardings (persons)')
fig.tight_layout()
FIGURE=ROOT/"figures"/"examples"/"13_13_heatmap.png"
FIGURE.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(FIGURE,dpi=130)
plt.close(fig)
print("Saved:",FIGURE.relative_to(ROOT))
