from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
hours=[9,10,11,12,13,14]
requests=[115,135,151,170,166,148]
latency=[75,82,96,128,112,88]
fig,axes=plt.subplots(2,1,sharex=True,figsize=(8,5.8),layout='constrained')
axes[0].plot(hours,requests,marker='o')
axes[0].set(title='Requests Received',ylabel='Requests')
axes[1].plot(hours,latency,marker='s',color='C1')
axes[1].set(title='Mean Response Time',ylabel='ms',xlabel='Hour')
axes[1].set_xticks(hours)
for ax in axes:ax.grid(axis='y',alpha=.22)
fig.savefig(ROOT/'figures'/'12_shared_axes.png',dpi=145)
plt.close(fig)
