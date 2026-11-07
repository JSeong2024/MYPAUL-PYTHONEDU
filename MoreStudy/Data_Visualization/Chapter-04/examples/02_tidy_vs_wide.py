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

wide = pd.DataFrame({"month": ["Jan", "Feb", "Mar"], "Central": [12, 15, 19], "North": [9, 11, 14]})
long = wide.melt(id_vars="month", var_name="branch", value_name="visitors_hundreds")
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
sns.lineplot(data=long, x="month", y="visitors_hundreds", hue="branch", marker="o", errorbar=None, ax=ax)
ax.set(title="Tidy data and multiple series", ylabel="Visitors (hundreds)")
fig.savefig(OUT / "02_tidy_vs_wide.png", dpi=145)
plt.close(fig)
print("Long-form rows:", len(long))
