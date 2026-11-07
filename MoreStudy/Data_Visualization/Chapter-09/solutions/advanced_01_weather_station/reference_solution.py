"""Reference implementation — Advanced 01 — Weather Station Review. Synthetic educational data."""
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
from core.analytics import weather_summary

OUTPUT = ROOT / 'output' / 'advanced_01_weather_station'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = weather_summary()
    good, bad, daily, slots = result
    daily.to_csv(output_dir / 'daily_summary.csv', index=False)
    bad.to_csv(output_dir / 'excluded_rows.csv', index=False)
    slots.to_csv(output_dir / 'coverage.csv', index=False)
    fig, axes = plt.subplots(2,1,figsize=(11,7),layout='constrained')
    for key, part in daily.groupby('region'):
        axes[0].plot(part['date'],part['temperature_c'],marker='.',markersize=3,label=key)
    axes[0].set(title='Daily Mean Temperature by Region',ylabel='Temperature (C)')
    axes[0].legend(ncol=4)
    p=slots.groupby('station_id')['available'].mean().sort_values()
    axes[1].barh(p.index,p.values*100)
    axes[1].set(xlim=(0,105),xlabel='Valid coverage (%)',title='Expected Observation Slot Coverage')
    fig.savefig(output_dir/'overview.png',dpi=140);plt.close(fig)
    metrics={'valid_rows':len(good),'excluded_rows':len(bad),'expected_slots':len(slots),'observed_slots':int(slots.available.sum())}
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
