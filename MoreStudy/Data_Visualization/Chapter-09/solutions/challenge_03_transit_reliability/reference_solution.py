"""Reference implementation — Challenge 03 — City Transit Reliability Audit. Synthetic educational data."""
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
from core.analytics import transit_summary

OUTPUT = ROOT / 'output' / 'challenge_03_transit_reliability'


def build_report(output_dir: Path = OUTPUT) -> dict:
    output_dir.mkdir(parents=True,exist_ok=True)
    result = transit_summary()
    import hashlib
    good,bad,daily,slots,incidents=result
    daily.to_csv(output_dir/'daily_summary.csv',index=False)
    slots.to_csv(output_dir/'coverage.csv',index=False)
    bad.to_csv(output_dir/'excluded_rows.csv',index=False)
    incidents.to_csv(output_dir/'incidents.csv',index=False)
    coverage=slots.groupby('stop_id').available.mean().sort_values()
    summed=good.groupby('line').boardings.sum().sort_index()
    heat=good.assign(hour=good['_parsed'].dt.hour).pivot_table(index='stop_id',columns='hour',values='boardings',aggfunc='mean')
    fig,axes=plt.subplots(2,2,figsize=(14,9),layout='constrained')
    axes[0,0].bar(summed.index,summed.values)
    axes[0,0].set(title='Boardings by Line',ylabel='Validated boardings (persons)')
    axes[0,1].barh(coverage.index,coverage.values*100)
    axes[0,1].set(title='Expected Slot Coverage',xlabel='Coverage (%)',xlim=(0,105))
    im=axes[1,0].imshow(heat.to_numpy(),aspect='auto',origin='upper')
    axes[1,0].set(title='Mean Boardings: Stop x Hour',yticks=range(len(heat)),yticklabels=heat.index,xticks=range(len(heat.columns)),xticklabels=heat.columns)
    fig.colorbar(im,ax=axes[1,0],label='Mean boardings (persons)')
    labels=incidents.category.value_counts().sort_index()
    axes[1,1].bar(labels.index,labels.values)
    axes[1,1].set(title='Reported Incident Counts',ylabel='Incidents (count)')
    fig.savefig(output_dir/'overview.png',dpi=150);plt.close(fig)
    # Canonical hash is for accepted tabular values, independent of output location.
    stable=good[['event_id','stop_id','timestamp_kst','boardings','delay_min']].sort_values('event_id')
    digest=hashlib.sha256(stable.to_csv(index=False,lineterminator='\n').encode('utf-8')).hexdigest()
    metrics={'valid_rows':len(good),'excluded_rows':len(bad),'expected_slots':len(slots),'observed_slots':int(slots.available.sum()),'total_boardings':int(good.boardings.sum()),'incidents':len(incidents),'accepted_data_sha256':digest}
    assert metrics['observed_slots']==metrics['valid_rows'], 'Coverage mismatch'
    assert len(bad)+len(good)==len(pd.read_csv(ROOT/'data'/'transit_operations.csv'))
    (output_dir/'report.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics


if __name__=='__main__':
    print(json.dumps(build_report(),ensure_ascii=False,indent=2))
