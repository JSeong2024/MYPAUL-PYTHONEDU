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
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
sns.lineplot(data=df, x="hour", y="response_ms", hue="service", estimator="mean", errorbar=None, marker="o", ax=ax)
ax.set(title="Mean latency per hour", xlabel="Hour", ylabel="Mean response (ms)")
fig.savefig(OUT / "04_lineplot_estimator.png", dpi=145)
plt.close(fig)
print("Unique hours:", df.hour.nunique())
