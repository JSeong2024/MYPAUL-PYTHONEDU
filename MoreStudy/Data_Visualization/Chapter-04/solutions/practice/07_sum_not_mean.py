"""Coding Practice: 매장별 매출 합계를 직접 집계한 뒤 표시.

이 파일은 완성된 참조 구현입니다.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="colorblind")

df = pd.read_csv(DATA / "retail_orders.csv").query("status == 'Completed'")
fig, axes = plt.subplots(1,2,figsize=(11,4),layout="constrained")
sns.barplot(data=df,x="branch",y="revenue_krw",estimator="mean",errorbar=None,color="steelblue",ax=axes[0])
total=df.groupby("branch",as_index=False).revenue_krw.sum()
sns.barplot(data=total,x="branch",y="revenue_krw",errorbar=None,color="steelblue",ax=axes[1])
axes[0].set(title="Mean per order line",ylabel="Mean (KRW)")
axes[1].set(title="Total completed revenue",ylabel="Total (KRW)")
fig.savefig(OUT / "07_barplot_mean_vs_sum.png",dpi=145)
plt.close(fig)
