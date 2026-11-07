from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

values = [80, 85, 90]
labels = ["A", "B", "C"]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
axes[0].bar(labels, values)
axes[0].set(title="Length (Bar)", ylabel="Count", ylim=(0, 110))
axes[1].scatter(labels, [1, 1, 1], s=[v**2 / 6 for v in values])
axes[1].set(title="Marker Area (Illustration)", ylim=(.6, 1.4))
axes[1].set_yticks([])
fig.suptitle("The Encoding Changes Perception")
fig.tight_layout()
fig.savefig(OUTPUT / "03_visual_encoding.png", dpi=150)
plt.close(fig)
print("Values:", values)
