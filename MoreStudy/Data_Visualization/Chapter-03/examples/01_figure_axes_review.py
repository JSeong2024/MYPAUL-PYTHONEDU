from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

# Chapter 01 복습: Figure 전체와 단일 Axes
fig, ax = plt.subplots(figsize=(7, 3.8), layout="constrained")
ax.plot([1, 2, 3, 4], [12, 16, 13, 19], marker="o")
ax.set(title="Weekly Visits", xlabel="Week", ylabel="Visitors (hundreds)")
ax.set_xticks([1, 2, 3, 4])
ax.grid(axis="y", alpha=0.25)
fig.savefig(ROOT / "figures" / "01_figure_axes.png", dpi=150)
plt.close(fig)
