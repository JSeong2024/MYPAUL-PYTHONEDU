"""Shared, deterministic CSV/model utilities for Summary Part 01 reference implementations."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import re
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, fbeta_score, precision_score, recall_score, balanced_accuracy_score, accuracy_score
from sklearn.model_selection import GroupShuffleSplit


def read_csv(name, columns):
    path = Path(name)
    if not path.is_file():
        raise ValueError(f'{name}: missing input file')
    with path.open(encoding='utf-8-sig', newline='') as stream:
        header = next(csv.reader(stream), None)
    if header is None or any(c not in header for c in columns) or len(header) != len(set(header)):
        raise ValueError(f'{name}: missing/duplicate columns')
    return pd.read_csv(path, dtype='string', keep_default_na=False, encoding='utf-8-sig')


def finite(value):
    try:
        num = float(value)
    except (ValueError, TypeError, OverflowError):
        return None
    return num if math.isfinite(num) else None


def integer(value, lo=0):
    if not isinstance(value, str) or not re.fullmatch(r'[+-]?\d+', value.strip()):
        return None
    val = int(value)
    return val if val >= lo else None


def date_str(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return None
    try:
        ts = pd.Timestamp(value)
    except (ValueError, TypeError):
        return None
    return value if ts.strftime('%Y-%m-%d') == value else None


def save_csv(name, rows, columns=None):
    if isinstance(rows, pd.DataFrame):
        if columns: rows = rows.loc[:, columns]
        rows.to_csv(name, index=False, encoding='utf-8', lineterminator='\n')
        return
    with open(name,'w',encoding='utf-8',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=columns,lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def save_json(name, obj):
    Path(name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n', encoding='utf-8')


def metric(y, pred, beta=1):
    y=np.asarray(y,dtype=int); pred=np.asarray(pred,dtype=int)
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    # Some metrics are mathematically undefined with zero denominator; retain counts.
    precision=float(precision_score(y,pred,zero_division=0))
    recall=float(recall_score(y,pred,zero_division=0))
    fb=float(fbeta_score(y,pred,beta=beta,zero_division=0))
    return dict(tp=int(tp),fp=int(fp),fn=int(fn),tn=int(tn),precision=precision,recall=recall,**{f'f{beta}':fb},positive_support=int(np.sum(y==1)),predicted_positives=int(np.sum(pred==1)),precision_defined=bool(tp+fp),recall_defined=bool(tp+fn))


def group_partition(df, key, seed=42):
    # First 20% groups test; then 25% of remainder validation => 60:20:20.
    groups=df[key].astype(str)
    first=GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed)
    pool_idx,test_idx=next(first.split(df,groups=groups))
    pool=df.iloc[pool_idx]
    second=GroupShuffleSplit(n_splits=1,test_size=0.25,random_state=seed)
    train_rel,val_rel=next(second.split(pool,groups=pool[key].astype(str)))
    train=pool.iloc[train_rel].copy();val=pool.iloc[val_rel].copy();test=df.iloc[test_idx].copy()
    keys=[set(f[key]) for f in (train,val,test)]
    if keys[0]&keys[1] or keys[0]&keys[2] or keys[1]&keys[2]:
        raise AssertionError('group leakage')
    return train,val,test


def regression_metrics(y,p):
    err=np.asarray(y,dtype=float)-np.asarray(p,dtype=float)
    return {'mae':float(np.mean(abs(err))),'rmse':float(np.sqrt(np.mean(err**2)))}


def valid_record_id(value):
    return isinstance(value,str) and bool(value.strip())


def atomic_bundle(target_dir, build_fn):
    """Stage + rollback a directory generation; no in-place writes before success.

    Multiple files cannot be installed atomically individually; swapping a complete
    result directory via rename + rollback keeps previous result on most failures.
    """
    import tempfile
    import os
    import shutil
    target=Path(target_dir).resolve(); parent=target.parent
    with tempfile.TemporaryDirectory(prefix='.summary-stage-',dir=parent) as tmp:
        stage=Path(tmp)/'new'; stage.mkdir()
        build_fn(stage)
        if not any(stage.iterdir()):
            raise ValueError('no output generated')
        backup=Path(tmp)/'backup'
        had_previous=target.exists()
        if had_previous: os.replace(target,backup)
        try:
            os.replace(stage,target)
        except Exception:
            if had_previous: os.replace(backup,target)
            raise
        # Backup is automatically cleaned once new directory is in place.
