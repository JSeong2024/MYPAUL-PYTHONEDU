from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)
import pandas as pd

frame = pd.read_csv(ROOT / "data" / "library_visits.csv", parse_dates=["date"])
daily = frame.groupby("date", as_index=False)[["visitors", "new_members"]].sum()
fig, axes = plt.subplots(2, 1, figsize=(8.4, 5.8), sharex=True)
axes[0].plot(daily["date"], daily["visitors"], marker="o", markersize=3)
axes[0].set(ylabel="Visitors (people)", title="Same Timeline, Separate Scales")
axes[1].plot(daily["date"], daily["new_members"], marker="o", markersize=3)
axes[1].set(ylabel="New members (people)", xlabel="Date")
for ax in axes: ax.grid(alpha=.2)
axes[1].tick_params(axis="x", rotation=30)
fig.tight_layout()
fig.savefig(OUTPUT / "13_dual_axis_alternative.png", dpi=150)
plt.close(fig)
print("Daily rows:", len(daily))
