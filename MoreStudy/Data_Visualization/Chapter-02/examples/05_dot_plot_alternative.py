from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

values = [80, 85]
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.scatter(values, ["A", "B"], s=105)
ax.set(xlim=(76, 90), title="Compare Close Values with a Dot Plot", xlabel="Score (points)")
ax.grid(axis="x", alpha=.25)
fig.tight_layout()
fig.savefig(OUTPUT / "05_dot_plot_alternative.png", dpi=150)
plt.close(fig)
print("Difference: 5 points (A=80, B=85)")
