"""Reference implementation — Advanced 02 — Retail Performance Review. Synthetic educational data."""
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
from core.analytics import retail_summary

OUTPUT = ROOT / 'output' / 'advanced_02_retail_performance'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = retail_summary()
    good, daily = result
    daily.to_csv(output_dir/'daily_summary.csv',index=False)
    fig,axes=plt.subplots(2,1,figsize=(11,7),layout='constrained')
    for sid,g in daily.groupby('store_id'):
        axes[0].plot(pd.to_datetime(g.date),g.revenue_krw,label=sid)
    axes[0].set(title='Daily Revenue',ylabel='Revenue (KRW)');axes[0].legend()
    totals=daily.groupby('store_id').revenue_krw.sum().sort_values()
    axes[1].barh(totals.index,totals.values)
    axes[1].set(title='Total Completed Revenue',xlabel='Revenue (KRW)')
    fig.savefig(output_dir/'overview.png',dpi=140);plt.close(fig)
    metrics={'valid_rows':len(good),'daily_rows':len(daily),'revenue_krw':int(good.revenue_krw.sum())}
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
