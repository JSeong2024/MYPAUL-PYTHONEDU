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

df=pd.read_csv(DATA/"retail_orders.csv").query("status == 'Completed'")
fig,ax=plt.subplots(figsize=(8,4.5),layout="constrained")
sns.boxplot(data=df,x="category",y="revenue_krw",hue="channel",palette="colorblind",ax=ax)
ax.set(title="Consistent channel colors",ylabel="Completed order value (KRW)")
ax.tick_params(axis="x",rotation=25)
ax.legend(title="Channel",bbox_to_anchor=(1.02,1),loc="upper left")
fig.savefig(OUT/"18_palette_legend.png",dpi=145,bbox_inches="tight")
plt.close(fig)
