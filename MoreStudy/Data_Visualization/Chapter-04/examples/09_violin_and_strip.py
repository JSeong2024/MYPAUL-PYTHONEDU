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

df = pd.read_csv(DATA / "service_requests.csv")
sample = df.sample(110,random_state=12)
fig,axes=plt.subplots(1,2,figsize=(11,4),layout="constrained")
sns.violinplot(data=df,x="service",y="response_ms",inner="quart",cut=0,color="lightblue",ax=axes[0])
sns.stripplot(data=sample,x="service",y="response_ms",jitter=.22,alpha=.45,size=3,color="black",ax=axes[1])
axes[0].set(title="Violin: smoothed distribution")
axes[1].set(title="Strip: 110 observed points")
fig.savefig(OUT/"09_violin_and_strip.png",dpi=145)
plt.close(fig)
