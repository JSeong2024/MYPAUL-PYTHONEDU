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

df = pd.read_csv(DATA / "retail_orders.csv")
fig, axes = plt.subplots(1,2,figsize=(10,3.8),layout="constrained")
sns.countplot(data=df,x="channel",color="steelblue",ax=axes[0])
sns.countplot(data=df,x="channel",hue="status",ax=axes[1])
axes[0].set(title="All order lines",ylabel="Count")
axes[1].set(title="Grouped by status",ylabel="Count")
fig.savefig(OUT / "06_countplot.png",dpi=145)
plt.close(fig)
