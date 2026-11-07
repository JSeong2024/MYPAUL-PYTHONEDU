from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
site_a = [120, 140, 138, 167, 185, 201]
site_b = [100, 118, 130, 142, 148, 174]

fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
ax.plot(months, site_a, marker="o", linewidth=2, label="Site A")
ax.plot(months, site_b, marker="s", linewidth=2, label="Site B")
ax.set(title="Monthly Visits by Site", xlabel="Month", ylabel="Visits")
ax.legend(title="Location")
ax.grid(axis="y", alpha=0.25)
fig.savefig(ROOT / "figures" / "02_multiple_lines.png", dpi=150)
plt.close(fig)
