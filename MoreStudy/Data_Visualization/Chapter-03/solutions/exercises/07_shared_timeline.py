from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
hours=[8,9,10,11,12];temperature=[21,22,23,25,24];humidity=[47,45,48,51,49]
fig,axes=plt.subplots(2,1,sharex=True,figsize=(8,5),layout='constrained')
axes[0].plot(hours,temperature,marker='o')
axes[0].set(title='Temperature',ylabel='°C')
axes[1].plot(hours,humidity,marker='s')
axes[1].set(title='Humidity',xlabel='Hour',ylabel='%')
axes[0].set_xticks(hours);axes[1].set_xticks(hours)
# A single shared x-axis can also be requested in the initial subplots() call.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_07.png',dpi=145)
plt.close(fig)
