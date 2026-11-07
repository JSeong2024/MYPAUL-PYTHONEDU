from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
fig=plt.figure(figsize=(9,5.8),layout='constrained')
grid=fig.add_gridspec(2,2,width_ratios=[2,1])
ax_main=fig.add_subplot(grid[:,0])
ax_top=fig.add_subplot(grid[0,1])
ax_bottom=fig.add_subplot(grid[1,1])
ax_main.plot(np.arange(12),[20,21,25,22,23,27,24,29,30,28,32,31],marker='o')
ax_main.set(title='Weekly Throughput',xlabel='Observation',ylabel='Requests (thousands)')
ax_top.bar(['A','B','C'],[20,13,17])
ax_top.set(title='By Site',ylabel='Count')
ax_bottom.hist([45,50,55,62,63,67,68,71,73,74,78,81],bins=5,edgecolor='white')
ax_bottom.set(title='Distribution',xlabel='Measured Value')
fig.savefig(ROOT/'figures'/'17_gridspec.png',dpi=145)
plt.close(fig)
