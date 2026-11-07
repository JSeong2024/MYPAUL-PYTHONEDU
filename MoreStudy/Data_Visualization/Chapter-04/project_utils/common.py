from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def theme():
    sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")

def export(fig, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target, dpi=145, bbox_inches="tight")
    plt.close(fig)
    return target

def export_json(report, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return target
