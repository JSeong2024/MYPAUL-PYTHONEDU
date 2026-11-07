from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

(ROOT / "output").mkdir(exist_ok=True)

categories = ["Mon", "Tue", "Wed", "Thu"]
values = [35, 42, 39, 51]

fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
ax.bar(categories, values)
ax.set(title="Daily Check-ins", xlabel="Day", ylabel="Check-ins")
fig.savefig(ROOT / "figures" / "09_export_formats.png", dpi=150)
fig.savefig(ROOT / "output" / "09_export_formats.svg", bbox_inches="tight")
plt.close(fig)
print("Saved: PNG (raster), SVG (vector)")
