from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
hours=[9,10,11,12,13,14];orders=[13,16,27,31,25,18]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
ax.plot(hours,orders,marker='o')
i=max(range(len(orders)),key=lambda j:orders[j])
ax.annotate('Peak',xy=(hours[i],orders[i]),xytext=(0,24),textcoords='offset points',ha='center',arrowprops={'arrowstyle':'->'})
ax.set(title='Hourly Orders',xlabel='Hour',ylabel='Orders')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_06.png',dpi=145)
plt.close(fig)
