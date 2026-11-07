from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="colorblind")

df = pd.read_csv(DATA / "retail_orders.csv").query("status == 'Completed'").copy()
daily = df.groupby(["date", "channel"], as_index=False).revenue_krw.sum()
daily["date"] = pd.to_datetime(daily["date"], format="%Y-%m-%d")
g = sns.relplot(data=daily, x="date", y="revenue_krw", col="channel", kind="line", marker="o", errorbar=None, col_wrap=3, height=3, aspect=1.25)
g.set_axis_labels("Date", "Daily revenue (KRW)")
for ax in g.axes.flat:
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.tick_params(axis="x", rotation=35, labelsize=8)
g.figure.savefig(OUT / "05_relplot_facets.png", dpi=145, bbox_inches="tight")
plt.close(g.figure)
