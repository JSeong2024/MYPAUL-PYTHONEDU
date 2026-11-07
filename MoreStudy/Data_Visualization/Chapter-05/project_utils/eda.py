from pathlib import Path
import numpy as np
import pandas as pd

def get_data_path(file_name: str) -> Path:
    return Path(__file__).resolve().parents[1] / 'data' / file_name

def valid_deliveries(frame: pd.DataFrame) -> pd.DataFrame:
    required = {'shipment_id', 'carrier', 'zone', 'status', 'promised_days', 'actual_days'}
    if not required.issubset(frame):
        raise ValueError('필수 배송 열이 없습니다.')
    if frame['shipment_id'].duplicated().any():
        raise ValueError('중복 배송 ID가 있습니다.')
    df = frame.copy()
    df['promised_days'] = pd.to_numeric(df['promised_days'], errors='coerce')
    df['actual_days'] = pd.to_numeric(df['actual_days'], errors='coerce')
    mask = (df['status'].eq('delivered') & df['actual_days'].notna()
            & np.isfinite(df['actual_days']) & df['actual_days'].ge(0)
            & df['promised_days'].gt(0) & np.isfinite(df['promised_days']))
    valid = df.loc[mask].copy()
    valid['on_time'] = valid['actual_days'].le(valid['promised_days'])
    return valid

def valid_response_times(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    if df['ticket_id'].duplicated().any():
        raise ValueError('중복 문의 ID가 있습니다.')
    df['first_response_min'] = pd.to_numeric(df['first_response_min'],errors='coerce')
    return df.loc[df['first_response_min'].notna()
                  & np.isfinite(df['first_response_min'])
                  & df['first_response_min'].ge(0)].copy()

def validated_inspections(frame: pd.DataFrame):
    required={'inspection_id','plant','line','shift','thickness_mm','is_defective'}
    if not required.issubset(frame): raise ValueError('필수 품질 검사 열이 없습니다.')
    df=frame.copy()
    duplicated=df['inspection_id'].duplicated(keep='first')
    df=df.loc[~duplicated].copy()
    df['thickness_mm']=pd.to_numeric(df['thickness_mm'],errors='coerce')
    df['is_defective']=pd.to_numeric(df['is_defective'],errors='coerce')
    invalid_defect=(~df['is_defective'].isin([0,1]))
    if invalid_defect.any(): raise ValueError('불량 여부는 0 또는 1이어야 합니다.')
    df['is_defective']=df['is_defective'].astype(int)
    review = (df['thickness_mm'].isna() | ~np.isfinite(df['thickness_mm'])
              | ~df['thickness_mm'].between(8,12))
    df['measurement_review']=review
    return df,int(duplicated.sum())

def bootstrap_mean_ci(values, confidence=.95, resamples=1200, seed=17):
    data=np.asarray(values,dtype=float)
    data=data[np.isfinite(data)]
    if len(data)<2: return float('nan'), float('nan')
    if not (0 < confidence < 1) or resamples<=0: raise ValueError('CI 파라미터 확인')
    rng=np.random.default_rng(seed)
    means=np.mean(rng.choice(data,size=(resamples,len(data)),replace=True),axis=1)
    a=(1-confidence)/2
    return tuple(float(x) for x in np.quantile(means,[a,1-a]))

def wilson_interval(successes:int, total:int, z=1.96):
    if total<=0: return float('nan'),float('nan')
    if not 0<=successes<=total: raise ValueError('성공 건수 범위를 벗어났습니다.')
    p=successes/total;d=1+z*z/total
    mid=(p+z*z/(2*total))/d
    half=z*np.sqrt((p*(1-p)+z*z/(4*total))/total)/d
    return float(mid-half),float(mid+half)
