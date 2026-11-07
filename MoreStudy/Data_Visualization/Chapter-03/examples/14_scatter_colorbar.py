from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
loads=[20,35,43,50,60,71,80,89]
latency=[95,110,133,145,190,225,315,410]
temp=[24,26,25,28,29,31,33,34]
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
dots=ax.scatter(loads,latency,c=temp,cmap='viridis',s=90,edgecolor='black',linewidth=.3)
fig.colorbar(dots,ax=ax,label='Device temperature (°C)')
ax.set(title='Load and Latency',xlabel='CPU Load (%)',ylabel='Response Time (ms)')
ax.grid(alpha=.2)
fig.savefig(ROOT/'figures'/'15_scatter_colorbar.png',dpi=145)
plt.close(fig)
