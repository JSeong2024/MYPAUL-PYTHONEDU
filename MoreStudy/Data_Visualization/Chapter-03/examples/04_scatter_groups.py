from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt

weekday_temp = [15, 17, 19, 21, 23, 25]
weekday_visits = [120, 145, 150, 185, 201, 223]
weekend_temp = [16, 19, 22, 24]
weekend_visits = [170, 210, 230, 265]

fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
ax.scatter(weekday_temp, weekday_visits, s=65, label="Weekday", alpha=0.8)
ax.scatter(weekend_temp, weekend_visits, s=65, label="Weekend", alpha=0.8)
ax.set(title="Temperature vs Visits", xlabel="Temperature (°C)", ylabel="Visitors")
ax.legend()
ax.grid(alpha=0.2)
fig.savefig(ROOT / "figures" / "04_scatter_groups.png", dpi=150)
plt.close(fig)
