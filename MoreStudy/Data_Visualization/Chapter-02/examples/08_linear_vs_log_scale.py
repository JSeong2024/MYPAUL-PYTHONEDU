from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

labels = ["Small", "Medium", "Large"]
values = [12, 120, 1200]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
for ax in axes:
    ax.plot(labels, values, marker="o")
    ax.set_ylabel("Positive count")
axes[0].set(title="Linear Y Axis")
axes[1].set_yscale("log")
axes[1].set(title="Log Y Axis (Explicit)")
fig.tight_layout()
fig.savefig(OUTPUT / "08_linear_vs_log_scale.png", dpi=150)
plt.close(fig)
print("Values: 12, 120, 1200 (10x steps)")
