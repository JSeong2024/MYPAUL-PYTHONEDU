from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

weeks = [1, 2, 3, 4, 5, 6]
requests = [120, 132, 148, 184, 166, 181]

fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
ax.plot(weeks, requests, marker="o")
ax.annotate("Campaign", xy=(4, 184), xytext=(4.6, 199),
            arrowprops={"arrowstyle": "->"})
ax.set(title="Weekly Requests", xlabel="Week", ylabel="Requests")
ax.set_xticks(weeks)
ax.set_ylim(100, 220)
ax.grid(axis="y", alpha=0.2)
fig.savefig(ROOT / "figures" / "07_annotation.png", dpi=150)
plt.close(fig)
