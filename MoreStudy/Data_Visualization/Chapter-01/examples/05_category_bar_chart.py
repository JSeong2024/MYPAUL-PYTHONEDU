from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
frame = pd.read_csv(ROOT / "data" / "park_visits.csv")
frame["weather"] = frame["rainfall_mm"].gt(0).map({True: "Rainy", False: "Dry"})
summary = frame.groupby("weather")["visitors"].mean().reindex(["Dry", "Rainy"])

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.bar(summary.index, summary.values)
ax.set(title="Average Visitors by Rain Status", xlabel="Day Type", ylabel="Average visitors (people/day)")
ax.set_ylim(bottom=0)  # 막대의 길이를 비교할 때는 0 기준을 권장합니다.
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
out = ROOT / "output" / "05_bar_chart.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
for label, value in summary.items():
    print(f"{label}: {value:.1f}")
