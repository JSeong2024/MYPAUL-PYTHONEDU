from pathlib import Path
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
months=['Jan','Feb','Mar','Apr','May']
units=[83,97,112,105,125]
# Context confines style adjustments to this figure.
with plt.rc_context({'axes.spines.top':False,'axes.spines.right':False,'grid.alpha':0.2}):
    fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
    ax.plot(months,units,color='#2C648D',linewidth=2.2,marker='o')
    ax.grid(axis='y')
    ax.set(title='Monthly Output',xlabel='Month',ylabel='Units')
    fig.savefig(ROOT/'figures'/'16_style_context.png',dpi=145)
    plt.close(fig)
