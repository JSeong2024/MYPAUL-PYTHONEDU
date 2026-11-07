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

df=pd.read_csv(DATA/"service_requests.csv")
pivot=df.pivot_table(index="service",columns="hour",values="response_ms",aggfunc="median")
fig,ax=plt.subplots(figsize=(11,4.5),layout="constrained")
sns.heatmap(pivot,cmap="YlGnBu",cbar_kws={"label":"Median response (ms)"},ax=ax)
ax.set(title="Median response by service and hour",xlabel="Hour",ylabel="Service")
fig.savefig(OUT/"17_heatmap_pivot.png",dpi=145)
plt.close(fig)
