"""Reference implementation — Advanced 03 — Service Reliability Review. Synthetic educational data."""
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
from core.analytics import latency_summary

OUTPUT = ROOT / 'output' / 'advanced_03_service_reliability'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = latency_summary()
    good, summary = result
    summary.to_csv(output_dir/'service_summary.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
    axes[0].bar(summary.service,summary.p95_ms)
    axes[0].set(title='P95 Latency by Service',ylabel='Latency (ms)')
    axes[1].bar(summary.service,summary.error_rate*100)
    axes[1].set(title='Error Rate by Service',ylabel='Error rate (%)')
    fig.savefig(output_dir/'overview.png',dpi=140);plt.close(fig)
    metrics={'valid_rows':len(good),'services':len(summary),'error_rows':int(good.is_error.sum())}
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
