from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="colorblind")

df=pd.read_csv(DATA/"library_visits.csv")
cols=["visitors","new_members","open_hours"]
corr=df[cols].corr(numeric_only=True)
fig,ax=plt.subplots(figsize=(6.5,4.5),layout="constrained")
sns.heatmap(corr,cmap="vlag",vmin=-1,vmax=1,center=0,annot=True,fmt=".2f",square=True,ax=ax)
ax.set(title="Linear correlation (Pearson)")
fig.savefig(OUT/"16_heatmap_corr.png",dpi=145)
plt.close(fig)
