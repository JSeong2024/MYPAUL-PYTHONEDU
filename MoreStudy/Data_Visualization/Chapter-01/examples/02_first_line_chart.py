from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TEMPERATURES = [21.5, 23.0, 22.4, 25.1, 26.3, 24.8, 23.2]
OUTPUT = Path(__file__).resolve().parents[1] / "output" / "02_first_line_chart.png"

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(DAYS, TEMPERATURES, marker="o", linewidth=2)
ax.set(title="Weekly Temperature (Example)", xlabel="Day", ylabel="Temperature (°C)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT, dpi=150)
plt.close(fig)
print("Saved:", OUTPUT.name)
print("Highest:", max(TEMPERATURES), "°C")
