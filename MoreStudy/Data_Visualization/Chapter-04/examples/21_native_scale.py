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

df=pd.DataFrame({"year":[2022,2023,2025],"sales":[100,130,170]})
fig,axes=plt.subplots(1,2,figsize=(10,4),layout="constrained")
sns.barplot(data=df,x="year",y="sales",color="steelblue",errorbar=None,ax=axes[0])
sns.barplot(data=df,x="year",y="sales",native_scale=True,color="steelblue",errorbar=None,ax=axes[1])
axes[0].set(title="Categorical spacing")
axes[1].set(title="Native numerical spacing")
fig.savefig(OUT/"21_native_scale.png",dpi=145)
plt.close(fig)
