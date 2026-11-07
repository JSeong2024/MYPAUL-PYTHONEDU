from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

waiting_minutes = [3, 4, 5, 5, 6, 7, 7, 8, 8, 9, 10, 11, 12, 13, 14, 15, 19, 22]

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True, layout="constrained")
for ax, bins in zip(axes, [4, 9]):
    ax.hist(waiting_minutes, bins=bins, edgecolor="white")
    ax.set(title=f"Histogram (bins={bins})", xlabel="Wait time (min)")
    ax.grid(axis="y", alpha=0.2)
axes[0].set_ylabel("Count")
fig.savefig(ROOT / "figures" / "06_histogram_bins.png", dpi=150)
plt.close(fig)
