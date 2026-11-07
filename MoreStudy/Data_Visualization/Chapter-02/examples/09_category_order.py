from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

original = {"East": 75, "West": 120, "North": 91, "South": 160}
ordered = sorted(original.items(), key=lambda item: item[1], reverse=True)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
axes[0].bar(list(original), list(original.values()))
axes[0].set(title="Unsorted Categories", ylim=(0, 185))
axes[1].bar([x[0] for x in ordered], [x[1] for x in ordered])
axes[1].set(title="Sorted by Value", ylim=(0, 185))
fig.tight_layout()
fig.savefig(OUTPUT / "09_category_order.png", dpi=150)
plt.close(fig)
print("Ranked:", [name for name, _ in ordered])
