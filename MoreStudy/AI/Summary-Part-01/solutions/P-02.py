"""P-02: week-isolated municipal demand forecasting and residual audit."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from common import read_csv, date_str, finite, integer, save_csv, regression_metrics

FEATURES=['last_week_kg','planned_events','holiday_days']; TARGET='next_week_kg'


def load():
    raw=read_csv('weekly_waste.csv',['zone_id','forecast_week',*FEATURES,TARGET]); valid=[]; seen=set(); rejected=[]
    for idx,r in raw.iterrows():
        z,w=str(r['zone_id']),str(r['forecast_week'])
        reason=None
        if not z or date_str(w) is None or pd.Timestamp(w).dayofweek!=0:reason='INVALID_KEY_OR_WEEK'
        values={k:(integer(str(r[k])) if k in ('planned_events','holiday_days') else finite(r[k])) for k in [*FEATURES,TARGET]}
        if any(v is None or v<0 for v in values.values()):reason=reason or 'INVALID_VALUE'
        if (z,w) in seen: reason=reason or 'DUPLICATE_RECORD'
        if reason:rejected.append((idx+2,reason));continue
        seen.add((z,w));valid.append({'zone_id':z,'forecast_week':w,**values})
    df=pd.DataFrame(valid)
    if df.empty or df.forecast_week.nunique()<15:raise ValueError('at least 15 unique weeks required')
    return df.sort_values(['forecast_week','zone_id']).reset_index(drop=True),rejected


def main():
    df,rejected=load(); weeks=sorted(df.forecast_week.unique());w=len(weeks); a=int(.6*w);b=a+int(.2*w)
    tr=df[df.forecast_week.isin(weeks[:a])]; val=df[df.forecast_week.isin(weeks[a:b])];te=df[df.forecast_week.isin(weeks[b:])]
    if min(len(tr),len(val),len(te))==0:raise ValueError('empty train/validation/test interval')
    experiments=[]
    for alpha in (.1,1.0,10.0):
        pipe=Pipeline([('scaler',StandardScaler()),('model',Ridge(alpha=alpha))])
        pipe.fit(tr[FEATURES],tr[TARGET]); err=regression_metrics(val[TARGET],pipe.predict(val[FEATURES]))['mae']
        experiments.append((err,alpha,pipe))
    _,alpha,best=min(experiments,key=lambda x:(x[0],x[1]))
    pred=best.predict(te[FEATURES]);y=te[TARGET].to_numpy(dtype=float);base=te['last_week_kg'].to_numpy(dtype=float)
    result=te[['zone_id','forecast_week']].copy()
    result['actual']=y;result['predicted']=pred;result['baseline']=base;result['residual']=y-pred
    result=result.round(4)
    save_csv('test_predictions.csv',result)
    zones=[]
    for z,g in result.groupby('zone_id',sort=True):
        zones.append({'zone_id':z,'sample_count':len(g),'mae':f'{np.mean(abs(g.residual)):.4f}',
                      'mean_residual':f'{g.residual.mean():.4f}'})
    save_csv('zone_metrics.csv',zones,['zone_id','sample_count','mae','mean_residual'])
    under=result[result.residual>0].sort_values(['residual','zone_id','forecast_week'],ascending=[False,True,True]).head(5)
    save_csv('underprediction_top5.csv',under[['zone_id','forecast_week','actual','predicted','residual']])
    ridge=regression_metrics(y,pred);baseline=regression_metrics(y,base)
    largest=max(zones,key=lambda z:float(z['mae']))
    Path('report.md').write_text(
        '# 주간 폐기물 수요 예측\n\n'
        f'유효 주차 {w}개, Train {len(tr)}행 / Validation {len(val)}행 / Test {len(te)}행. '
        f'정제 제외 {len(rejected)}행. 날짜가 다른 구간에서 중복되지 않습니다.\n\n'
        '입력: last_week_kg, planned_events, holiday_days. zone_id와 Target은 모델에 넣지 않았습니다.\n'
        f'선정 alpha: {alpha:.1f} (Validation MAE).\n'
        f'Test Ridge MAE {ridge["mae"]:.4f}, RMSE {ridge["rmse"]:.4f}.\n'
        f'Test 직전 주 Baseline MAE {baseline["mae"]:.4f}, RMSE {baseline["rmse"]:.4f}.\n'
        f'평가 기간 중 MAE가 가장 큰 구역은 {largest["zone_id"]} ({largest["mae"]} kg)입니다.\n'
        '과소 예측이 큰 주에는 배차 및 인력이 부족해질 수 있습니다. 상위 사례를 검토하고 예비 차량 투입 기준을 따로 정해야 합니다.\n'
        '이 결과는 대상 기간의 관찰값이며 미래 일반화 성능을 보장하지 않습니다.\n',encoding='utf-8')


if __name__=='__main__':
    try:main()
    except ValueError as error:raise SystemExit(f'ERROR: {error}') from error
