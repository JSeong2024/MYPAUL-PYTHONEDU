"""Reference implementation — Advanced 05 — Metro Operations Audit. Synthetic educational data."""
from __future__ import annotations
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.analytics import metro_summary

OUTPUT = ROOT / 'output' / 'advanced_05_metro_operations'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = metro_summary()
    good,bad,daily,slots=result
    bad.to_csv(output_dir/'excluded_rows.csv',index=False)
    daily.to_csv(output_dir/'daily_summary.csv',index=False)
    slots.to_csv(output_dir/'coverage.csv',index=False)
    counts=good.groupby('station_name').boardings.sum().sort_values()
    cov=slots.groupby('station_id').available.mean().sort_values()
    fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    axes[0].barh(counts.index,counts.values)
    axes[0].set(title='Validated Boardings by Station',xlabel='Boardings (persons)')
    axes[1].barh(cov.index,cov.values*100)
    axes[1].set(title='Expected Slot Coverage',xlabel='Coverage (%)',xlim=(0,105))
    fig.savefig(output_dir/'overview.png',dpi=140);plt.close(fig)
    metrics={'valid_rows':len(good),'excluded_rows':len(bad),'expected_slots':len(slots),'observed_slots':int(slots.available.sum()),'total_boardings':int(good.boardings.sum())}
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
