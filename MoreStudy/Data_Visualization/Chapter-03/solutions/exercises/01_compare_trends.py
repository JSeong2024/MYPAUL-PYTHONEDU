from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT = Path(__file__).resolve().parents[2] / "output"
OUTPUT.mkdir(exist_ok=True)

months = ["Jan", "Feb", "Mar", "Apr"]
site_a = [120, 140, 150, 180]
site_b = [105, 131, 137, 160]
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
ax.plot(months, site_a, marker="o", label="Site A")
ax.plot(months, site_b, marker="s", label="Site B")
ax.set(title="Monthly Visits", xlabel="Month", ylabel="Visits")
ax.legend()
fig.savefig(OUTPUT / "exercise_01.png", dpi=150)
plt.close(fig)
