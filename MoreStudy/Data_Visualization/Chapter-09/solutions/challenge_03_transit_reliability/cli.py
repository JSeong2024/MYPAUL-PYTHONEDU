"""Challenge 03 reference CLI with strict input validation and deterministic exports."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from core.analytics import read_csv,transit_summary
from solutions.challenge_03_transit_reliability.reference_solution import build_report
from solutions.challenge_03_transit_reliability.reliability_engine import (
    validate_references,quality_gate,daily_completeness,export_manifest,Policy)


def run(output_dir:Path, requested_stops:list[str]|None=None)->dict:
    stops=read_csv('transit_stops.csv');incidents=read_csv('transit_incidents.csv')
    validate_references(stops,incidents)
    good,bad,daily,slots,incidents=transit_summary()
    policy=Policy()
    quality_gate(good,bad,slots,len(read_csv('transit_operations.csv')),policy)
    selected=set(stops.stop_id.tolist() if requested_stops is None else requested_stops)
    unknown=selected-set(stops.stop_id)
    if unknown:raise ValueError(f'Unknown stop IDs: {sorted(unknown)}')
    if not selected:raise ValueError('At least one stop is required')
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    # A run-specific output folder avoids silently mixing old results with new filters.
    a=good[good.stop_id.isin(selected)].copy()
    s=slots[slots.stop_id.isin(selected)].copy()
    d=daily[daily.stop_id.isin(selected)].copy()
    i=incidents[incidents.stop_id.isin(selected)].copy()
    b=bad[bad.stop_id.isin(selected)].copy()
    completeness=daily_completeness(s,policy)
    # Descriptive aggregate for complete days only.
    complete=d.drop(columns=['complete']).merge(completeness[['stop_id','date','complete']],on=['stop_id','date'],validate='one_to_one')
    complete=complete[complete.complete].copy()
    month=complete.groupby('line',as_index=False).agg(boardings=('boardings','sum'),complete_days=('date','size'))
    if month.empty:raise ValueError('No fully observed day for the chosen stops')
    month.to_csv(output_dir/'complete_day_totals.csv',index=False)
    completeness.to_csv(output_dir/'daily_completeness.csv',index=False)
    b.to_csv(output_dir/'excluded_rows.csv',index=False)
    i.to_csv(output_dir/'selected_incidents.csv',index=False)
    # The primary chart includes all selected stops; QA summary uses selected data.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,max(4,len(selected)*.5)))
    cover=s.groupby('stop_id').available.mean().sort_values()
    ax.barh(cover.index,cover.values*100)
    ax.set(xlim=(0,105),xlabel='Coverage (%)',title='Validated Expected-Slot Coverage')
    fig.tight_layout();fig.savefig(output_dir/'selected_coverage.png',dpi=140);plt.close(fig)
    report={'requested_stops':sorted(selected),'expected_slots':int(len(s)),
            'accepted_slots':int(s.available.sum()),'coverage':float(s.available.mean()),
            'complete_stop_days':int(completeness.complete.sum()),
            'all_stop_days':len(completeness),'excluded_rows_with_selected_ID':len(b)}
    (output_dir/'report.json').write_text(json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    input_files={name:ROOT/'data'/name for name in ['transit_stops.csv','transit_operations.csv','transit_incidents.csv']}
    export_manifest(output_dir,input_files,report)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='City Transit Reliability Audit — synthetic data')
    parser.add_argument('--output',type=Path,default=ROOT/'output'/'challenge_03_cli')
    parser.add_argument('--stops',nargs='*',default=None)
    args=parser.parse_args()
    print(json.dumps(run(args.output,args.stops),ensure_ascii=False,indent=2))
