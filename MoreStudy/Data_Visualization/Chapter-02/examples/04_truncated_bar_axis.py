from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

values = [80, 85]
fig, axes = plt.subplots(1, 2, figsize=(9.2, 4))
for ax in axes:
    bars = ax.bar(["A", "B"], values)
    ax.bar_label(bars, padding=4)
    ax.set_ylabel("Score (points)")
axes[0].set(title="Zero Baseline", ylim=(0, 100))
axes[1].set(title="Truncated Bar Axis (Misleading)", ylim=(75, 100))
fig.tight_layout()
fig.savefig(OUTPUT / "04_truncated_bar_axis.png", dpi=150)
plt.close(fig)
print("Absolute difference:", values[1] - values[0], "points")
