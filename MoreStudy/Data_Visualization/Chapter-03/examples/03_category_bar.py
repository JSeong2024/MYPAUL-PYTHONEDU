from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

sales = {"Books": 235, "Stationery": 174, "Snacks": 132, "Drinks": 205}
items = sorted(sales.items(), key=lambda item: item[1])
names = [name for name, value in items]
values = [value for name, value in items]

fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
bars = ax.barh(names, values)
ax.bar_label(bars, padding=4)
ax.set(title="Sales by Category", xlabel="Orders")
ax.set_xlim(0, 270)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(ROOT / "figures" / "03_category_bar.png", dpi=150)
plt.close(fig)
