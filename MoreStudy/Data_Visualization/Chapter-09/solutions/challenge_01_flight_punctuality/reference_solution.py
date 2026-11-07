"""Reference implementation — Challenge 01 — Airport Punctuality Review. Synthetic educational data."""
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
from core.analytics import flight_summary

OUTPUT = ROOT / 'output' / 'challenge_01_flight_punctuality'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = flight_summary()
    good,daily=result
    daily.to_csv(output_dir/'daily_summary.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
    import seaborn as sns
    sns.boxplot(data=good,x='airport',y='delay_min',ax=axes[0],showfliers=False)
    axes[0].set(title='Flight Delay Distribution',ylabel='Delay (min)')
    for air,g in daily.groupby('airport'):
        axes[1].plot(pd.to_datetime(g.date),g.late_rate*100,label=air)
    axes[1].set(title='Daily Flights Delayed More Than 15 Minutes',ylabel='Delayed flights (%)')
    axes[1].legend()
    fig.savefig(output_dir/'overview.png',dpi=140);plt.close(fig)
    metrics={'flights':len(good),'late_flights':int(good.late_flag.sum()),'airports':int(good.airport.nunique())}
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
