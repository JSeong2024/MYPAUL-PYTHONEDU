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

df=pd.read_csv(DATA/"library_visits.csv",parse_dates=["date"])
days=pd.date_range(df.date.min(),df.date.max(),freq="D")
full=pd.MultiIndex.from_product([sorted(df.branch.unique()),days],names=["branch","date"]).to_frame(index=False)
full=full.merge(df,on=["branch","date"],how="left",validate="one_to_one")
fig,ax=plt.subplots(figsize=(9,4),layout="constrained")
east = full.loc[full.branch.eq("East")].sort_values("date")
sns.scatterplot(data=east, x="date", y="visitors", s=45, ax=ax)
# Matplotlib keeps NaN as a break rather than connecting across the gap.
ax.plot(east["date"], east["visitors"], color="steelblue", linewidth=1.5, alpha=.7)
ax.set(title="Missing record is not zero visitors",ylabel="Observed visitors")
fig.savefig(OUT/"19_missing_values.png",dpi=145)
plt.close(fig)
print("Missing observations:",int(full.visitors.isna().sum()))
