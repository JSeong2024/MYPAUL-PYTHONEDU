"""Coding Practice: 시간대별 평균 응답시간 표시, 신뢰구간은 숨김.

이 파일은 일부 코드가 비어 있습니다. TODO를 완성한 뒤 실행하세요.
"""
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
# TODO: 시간대별 평균 응답시간 표시, 신뢰구간은 숨김
raise NotImplementedError("TODO: 04_hour_mean")
ax.set(title="Mean latency per hour", xlabel="Hour", ylabel="Mean response (ms)")
fig.savefig(OUT / "04_lineplot_estimator.png", dpi=145)
plt.close(fig)
print("Unique hours:", df.hour.nunique())
