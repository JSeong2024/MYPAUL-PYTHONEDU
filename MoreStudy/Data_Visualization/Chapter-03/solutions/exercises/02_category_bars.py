from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT = Path(__file__).resolve().parents[2] / "output"
OUTPUT.mkdir(exist_ok=True)

orders = {"Books": 42, "Games": 63, "Music": 35, "Movies": 48}
items = sorted(orders.items(), key=lambda item: item[1])
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
bars = ax.barh([name for name, value in items], [value for name, value in items])
ax.bar_label(bars, padding=3)
ax.set(title="Orders by Category", xlabel="Orders", xlim=(0, 75))
fig.savefig(OUTPUT / "exercise_02.png", dpi=150)
plt.close(fig)
