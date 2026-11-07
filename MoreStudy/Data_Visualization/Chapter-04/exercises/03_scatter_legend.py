"""Coding Practice: hue와 style을 사용해 서비스와 우선순위 구분.

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

df = pd.read_csv(DATA / "service_requests.csv").sample(120, random_state=7)
fig, ax = plt.subplots(figsize=(8, 4.6), layout="constrained")
# TODO: hue와 style을 사용해 서비스와 우선순위 구분
raise NotImplementedError("TODO: 03_scatter_legend")
ax.set(title="Response time by hour", xlabel="Hour", ylabel="Response time (ms)")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
fig.savefig(OUT / "03_hue_style_size.png", dpi=145, bbox_inches="tight")
plt.close(fig)
