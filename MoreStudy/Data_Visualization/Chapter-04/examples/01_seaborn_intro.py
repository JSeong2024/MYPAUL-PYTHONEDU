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
completed = df.loc[df.status.eq("Completed")]
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
sns.countplot(data=completed, x="channel", color="steelblue", ax=ax)
ax.set(title="Completed orders by channel", xlabel="Channel", ylabel="Order lines")
fig.savefig(OUT / "01_seaborn_intro.png", dpi=145)
plt.close(fig)
print("Completed:", len(completed))
