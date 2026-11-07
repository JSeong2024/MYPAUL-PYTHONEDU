"""Coding Practice: 채널별 Facet 생성.

이 파일은 일부 코드가 비어 있습니다. TODO를 완성한 뒤 실행하세요.
"""
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
# TODO: 채널별 Facet 생성
raise NotImplementedError("TODO: 05_faceted_channels")
g.set_axis_labels("Date", "Daily revenue (KRW)")
for ax in g.axes.flat:
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.tick_params(axis="x", rotation=35, labelsize=8)
g.figure.savefig(OUT / "05_relplot_facets.png", dpi=145, bbox_inches="tight")
plt.close(g.figure)
