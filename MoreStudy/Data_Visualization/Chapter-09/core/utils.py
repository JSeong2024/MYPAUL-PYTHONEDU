"""Only transport helpers are shared; each project owns its analysis policy."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def arguments(script: str, project_id: str, extra=None):
    parser = argparse.ArgumentParser(description=script)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument('--data', type=Path, default=root/'projects'/project_id/'data')
    parser.add_argument('--output', type=Path, default=root/'output'/project_id)
    if extra:
        extra(parser)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    return args


def load(path: Path, columns):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    if not set(columns).issubset(df.columns) or len(df.columns)!=len(set(df.columns)):
        raise ValueError(f'{path.name}: 필수 열이 없거나 열 이름이 중복되었습니다: {columns}')
    return df


def save(df, path):
    df.to_csv(path, index=False, encoding='utf-8', float_format='%.4f')


def figure_start(w=10,h=5):
    fig,ax=plt.subplots(figsize=(w,h),dpi=125)
    ax.grid(alpha=.18)
    ax.set_axisbelow(True)
    return fig,ax


def finish(fig,path):
    fig.tight_layout()
    fig.savefig(path, dpi=125, metadata={'Software':'Matplotlib'})
    plt.close(fig)


def numeric(series):
    return pd.to_numeric(series,errors='coerce').replace([float('inf'), float('-inf')],float('nan'))


def kst(series):
    return pd.to_datetime(series,utc=True,errors='coerce').dt.tz_convert('Asia/Seoul')


def iso_day(frame,col='local_date',start=None,end=None):
    result=frame
    if start:result=result[result[col]>=start]
    if end:result=result[result[col]<=end]
    return result.copy()
