from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT = Path(__file__).resolve().parents[2] / "output"
OUTPUT.mkdir(exist_ok=True)

weeks = [1, 2, 3, 4]
visits = [60, 80, 75, 95]
revenue = [30, 38, 42, 47]
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
axes[0].plot(weeks, visits, marker="o")
axes[0].set(title="Visits", xlabel="Week", ylabel="People")
axes[1].bar(weeks, revenue)
axes[1].set(title="Revenue", xlabel="Week", ylabel="10k KRW")
fig.savefig(OUTPUT / "exercise_03.png", dpi=150)
plt.close(fig)
