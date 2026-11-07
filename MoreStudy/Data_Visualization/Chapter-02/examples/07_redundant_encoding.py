from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

labels = ["Complete", "Pending", "Failed"]
values = [18, 9, 3]
fig, ax = plt.subplots(figsize=(7.5, 3.7))
bars = ax.bar(labels, values, edgecolor="black")
for bar, pattern in zip(bars, ["", "//", "xx"]):
    bar.set_hatch(pattern)
ax.bar_label(bars, padding=3)
ax.set(title="Status Counts (Patterns + Text)", ylabel="Cases", ylim=(0, 22))
fig.tight_layout()
fig.savefig(OUTPUT / "07_redundant_encoding.png", dpi=150)
plt.close(fig)
print("Counts:", dict(zip(labels, values)))
