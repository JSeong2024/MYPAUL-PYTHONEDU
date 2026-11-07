from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

from math import sqrt

def wilson(k,n,z=1.96):
    p=k/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den
    radius=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return center-radius,center+radius

n=[10,100,1000];k=[1,10,100];intervals=[wilson(a,b) for a,b in zip(k,n)]
fig,ax=plt.subplots(figsize=(7,4))
for idx,(lo,hi) in enumerate(intervals):
    ax.errorbar(.1,idx,xerr=[[.1-lo],[hi-.1]],fmt='o',capsize=4,color='#337CA3')
ax.set(yticks=range(3),yticklabels=[f'n={x}' for x in n],xlabel='Observed defect share',title='Same rate, different uncertainty',xlim=(0,.45))
fig.tight_layout();fig.savefig(ROOT/'figures/15_sample_size_ci.png',dpi=145);plt.close(fig)
print('Intervals:',[(round(lo,3),round(hi,3)) for lo,hi in intervals])
