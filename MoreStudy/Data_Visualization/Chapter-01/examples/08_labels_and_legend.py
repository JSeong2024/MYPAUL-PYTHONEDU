from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEK_A = [15, 18, 20, 19, 22, 21, 17]
WEEK_B = [17, 16, 19, 23, 24, 20, 18]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(DAYS, WEEK_A, marker="o", label="Week A")
ax.plot(DAYS, WEEK_B, marker="s", label="Week B")
ax.set(title="Two Weeks: Temperature Comparison", xlabel="Day", ylabel="Temperature (°C)")
ax.legend()
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
out = Path(__file__).resolve().parents[1] / "output" / "08_labels_and_legend.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
print("Series:", 2)
