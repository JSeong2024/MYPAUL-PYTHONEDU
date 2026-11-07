"""Reference implementation — Challenge 02 — Electricity Load Audit. Synthetic educational data."""
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
from core.analytics import electricity_summary

OUTPUT = ROOT / 'output' / 'challenge_02_grid_incident'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = electricity_summary()
    good, bad, daily = result
    bad.to_csv(output_dir/'excluded_rows.csv',index=False)
    daily.to_csv(output_dir/'daily_summary.csv',index=False)
    fig,axes=plt.subplots(2,1,figsize=(11,7),layout='constrained')
    for region,g in good.groupby('region'):
        axes[0].plot(g.timestamp_kst,g.demand_mw,label=region,alpha=.8,linewidth=.7)
    axes[0].set(title='Hourly Power Demand (KST)',ylabel='Demand (MW)')
    axes[0].legend(ncol=4)
    for region,g in daily.groupby('region'):
        axes[1].plot(pd.to_datetime(g.date_kst),g.mean_demand_mw,label=region)
    axes[1].set(title='Daily Mean Demand',ylabel='Mean demand (MW)')
    fig.savefig(output_dir/'overview.png',dpi=140);plt.close(fig)
    metrics={'valid_rows':len(good),'excluded_rows':len(bad),'regions':int(good.region.nunique())}
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
