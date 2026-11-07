from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
load=[30,45,57,68,80];time=[80,98,110,180,240];temp=[22,24,27,29,31]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
sc=ax.scatter(load,time,c=temp,cmap='viridis',s=100)
fig.colorbar(sc,ax=ax,label='Device temp (°C)')
ax.set(title='Load vs Response',xlabel='Load (%)',ylabel='Response time (ms)')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_09.png',dpi=145)
plt.close(fig)
