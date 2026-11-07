from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
months=['Jan','Feb','Mar','Apr'];means=[12,15,14,18];error=[1.1,1.8,1.4,1.2]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
ax.errorbar(months,means,yerr=error,fmt='o-',capsize=4)
ax.set(title='Monthly Sensor Means',xlabel='Month',ylabel='Measured units')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_14.svg')
fig.savefig(ROOT/'output'/'practice_14.png',dpi=145)
plt.close(fig)
