from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
sizes=[1,10,100,1000,10000]
counts=[5,45,600,5600,58000]
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for ax in axes:
    ax.plot(sizes,counts,marker='o')
    ax.set(xlabel='Input rows',ylabel='Operations')
    ax.grid(alpha=.2)
axes[0].set(title='Linear Axes')
axes[1].set(xscale='log',yscale='log',title='Log-Log Axes')
fig.savefig(ROOT/'figures'/'13_axis_scales.png',dpi=145)
plt.close(fig)
