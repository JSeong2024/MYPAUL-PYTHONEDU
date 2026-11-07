from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT = Path(__file__).resolve().parents[1] / "output" / "03_figure_and_axes.png"
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot([1, 2, 3, 4], [12, 17, 15, 22], marker="o")
ax.set_title("Four Observations")
ax.set_xlabel("Observation Index")
ax.set_ylabel("Measured Value")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT, dpi=150)
plt.close(fig)
print("Figure contains:", len(fig.axes), "Axes")
