from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "output"
out.mkdir(parents=True, exist_ok=True)
fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.bar(["A", "B", "C"], [12, 17, 14])
ax.set(title="Simple Comparison", ylabel="Count (items)")
ax.set_ylim(bottom=0)
fig.tight_layout()
fig.savefig(out / "11_comparison.png", dpi=150)
fig.savefig(out / "11_comparison.svg")
plt.close(fig)
print("Saved: 11_comparison.png, 11_comparison.svg")
