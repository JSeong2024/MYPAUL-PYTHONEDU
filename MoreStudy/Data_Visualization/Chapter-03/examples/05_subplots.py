from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr"]
visitors = [120, 150, 140, 190]
revenue = [80, 110, 100, 145]

fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
axes[0].plot(months, visitors, marker="o")
axes[0].set(title="Monthly Visitors", ylabel="Visitors")
axes[1].bar(months, revenue)
axes[1].set(title="Monthly Revenue", ylabel="Revenue (10k KRW)")
fig.suptitle("Two Measures, Two Units")
fig.savefig(ROOT / "figures" / "05_subplots.png", dpi=150)
plt.close(fig)
