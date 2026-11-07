"""Advanced, deterministic, auditable quality gates for Challenge 03.

The dataset is synthetic. Reports are descriptive, not causal.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass(frozen=True)
class Policy:
    start: str = '2026-09-01'
    end: str = '2026-09-30'
    first_hour: int = 6
    last_hour: int = 22
    minimum_daily_coverage: float = 1.0


def validate_references(stops: pd.DataFrame, incidents: pd.DataFrame) -> None:
    expected={'stop_id','line','zone'}
    if not expected.issubset(stops.columns):raise ValueError('stops missing required columns')
    if stops.stop_id.isna().any() or stops.stop_id.duplicated().any():
        raise ValueError('duplicate or null stop ID')
    if not {'incident_id','stop_id','date','duration_min','category'}.issubset(incidents.columns):
        raise ValueError('incidents missing required columns')
    if incidents.incident_id.isna().any() or incidents.incident_id.duplicated().any():
        raise ValueError('duplicate or null incident ID')
    if not incidents.stop_id.isin(stops.stop_id).all():
        raise ValueError('incident linked to unknown stop')
    if incidents.duration_min.isna().any() or (incidents.duration_min<0).any():
        raise ValueError('invalid incident duration')


def quality_gate(accepted: pd.DataFrame, excluded: pd.DataFrame, slots: pd.DataFrame,
                 raw_count: int, policy: Policy=Policy()) -> None:
    if len(accepted)+len(excluded)!=raw_count:
        raise AssertionError('accounting identity violated')
    if len(accepted)!=int(slots.available.sum()):
        raise AssertionError('accepted records and coverage disagree')
    if slots.duplicated(['stop_id','date','hour']).any():
        raise AssertionError('expected slot duplicated')
    if accepted.duplicated(['stop_id','_parsed']).any():
        raise AssertionError('accepted duplicate slot')
    if not slots.observed.isin([0,1]).all():
        raise AssertionError('invalid expected slot count')
    expected_days=len(pd.date_range(policy.start,policy.end))
    expected_stops=slots.stop_id.nunique()
    expected_length=expected_days*expected_stops*(policy.last_hour-policy.first_hour+1)
    if len(slots)!=expected_length:
        raise AssertionError('incorrect expected time grid')


def daily_completeness(slots: pd.DataFrame, policy: Policy=Policy()) -> pd.DataFrame:
    daily=slots.groupby(['stop_id','date'],as_index=False).agg(valid_hours=('available','sum'),expected_hours=('available','size'))
    daily['coverage']=daily.valid_hours/daily.expected_hours
    daily['complete']=daily.coverage.ge(policy.minimum_daily_coverage)
    return daily


def export_manifest(output_dir: Path, inputs: dict[str,Path], metrics:dict) -> dict:
    output_dir=Path(output_dir)
    def digest(f:Path)->str:
        return hashlib.sha256(f.read_bytes()).hexdigest()
    data={'format_version':'1.0','input_files':{name:digest(path) for name,path in sorted(inputs.items())},
          'metrics':metrics,'report_files':{p.name:digest(p) for p in sorted(output_dir.iterdir()) if p.is_file() and p.name!='manifest.json'}}
    (output_dir/'manifest.json').write_text(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return data
