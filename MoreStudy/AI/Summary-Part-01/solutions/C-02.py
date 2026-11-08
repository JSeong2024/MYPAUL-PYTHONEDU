"""C-02: schema migration, strict incoming validation and protected result swap."""
from pathlib import Path
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from common import read_csv,date_str,finite,integer,save_csv,regression_metrics,atomic_bundle

HISTORY=['date','temperature_c','scheduled_events','is_weekend','visitors_next_day']
INCOMING=['date','temperature_f','scheduled_events','is_weekend']
FEATURES=['temperature_c','scheduled_events','is_weekend']


def history_data():
    raw=read_csv('history_v1.csv',HISTORY);rows=[];seen=set()
    for idx,r in raw.iterrows():
        date=date_str(str(r['date']));temp=finite(r['temperature_c']);event=integer(str(r['scheduled_events']));weekend=integer(str(r['is_weekend']));target=integer(str(r['visitors_next_day']))
        if date is None or date in seen or temp is None or event is None or weekend not in (0,1) or target is None:
            raise ValueError(f'history_v1.csv: invalid row {idx+2}')
        seen.add(date);rows.append(dict(date=date,temperature_c=temp,scheduled_events=event,is_weekend=weekend,visitors_next_day=target))
    df=pd.DataFrame(rows).sort_values('date').reset_index(drop=True)
    if len(df)<120:raise ValueError('history_v1.csv: at least 120 valid days required')
    return df


def clean_incoming():
    raw=read_csv('incoming_v2.csv',INCOMING); rows=[];rejected=[];seen=set()
    for idx,r in raw.iterrows():
        date=date_str(str(r['date']));temp=finite(r['temperature_f']);event=integer(str(r['scheduled_events']));weekend=integer(str(r['is_weekend']))
        error=None
        if date is None:error='INVALID_DATE'
        elif str(r['temperature_f']).strip()=='':error='MISSING_TEMPERATURE'
        elif temp is None:error='INVALID_TEMPERATURE'
        elif event is None or weekend not in (0,1):error='INVALID_FEATURE'
        elif date in seen:error='DUPLICATE_DATE'
        if error:rejected.append({'source_line':idx+2,'error_code':error});continue
        seen.add(date);rows.append(dict(date=date,temperature_c=(temp-32)*5/9,scheduled_events=event,is_weekend=weekend))
    return pd.DataFrame(rows,columns=['date',*FEATURES]),rejected


def main():
    hist=history_data();incoming,rejected=clean_incoming()
    n=len(hist);a=int(.6*n);b=a+int(.2*n)
    # A next-day target for a boundary day is not observable at that split's end.
    tr=hist.iloc[:a-1].copy();val=hist.iloc[a:b-1].copy();test=hist.iloc[b:].copy()
    if any(x.empty for x in (tr,val,test)):raise ValueError('empty validation interval')
    baseline=float(tr.visitors_next_day.mean());baseline_val=regression_metrics(val.visitors_next_day,np.full(len(val),baseline))['mae']
    model=Pipeline([('scaler',StandardScaler()),('model',Ridge(alpha=1.0))])
    model.fit(tr[FEATURES],tr.visitors_next_day)
    ridge_val=regression_metrics(val.visitors_next_day,model.predict(val[FEATURES]))['mae']
    chosen='baseline' if baseline_val<=ridge_val else 'ridge'
    test_prediction=np.full(len(test),baseline) if chosen=='baseline' else model.predict(test[FEATURES])
    m=regression_metrics(test.visitors_next_day,test_prediction)
    future=np.full(len(incoming),baseline) if chosen=='baseline' else (model.predict(incoming[FEATURES]) if len(incoming) else [])
    def build(stage):
        norm=incoming.copy()
        if not norm.empty:norm['temperature_c']=norm['temperature_c'].map(lambda v:f'{v:.4f}')
        save_csv(stage/'normalized_incoming.csv',norm,['date',*FEATURES])
        save_csv(stage/'rejected_rows.csv',rejected,['source_line','error_code'])
        save_csv(stage/'predictions.csv', [{'date':date,'predicted_visitors':f'{float(pred):.2f}'} for date,pred in zip(incoming.date,future)], ['date','predicted_visitors'])
        counts=Counter(x['error_code'] for x in rejected)
        stage.joinpath('recovery_report.md').write_text(
            '# 도서관 예측 시스템 복구\n\n'
            'incoming_v2의 temperature_f를 섭씨로 변환하고, 결측·잘못된 범위·중복 날짜를 거부했습니다.\n'
            f'정상 {len(incoming)}건 / 거부 {len(rejected)}건 ({dict(counts)}).\n'
            f'Validation Baseline MAE {baseline_val:.4f}, Ridge MAE {ridge_val:.4f}; 동점은 Baseline 선택. 최종: {chosen}.\n'
            f'과거 Test MAE {m["mae"]:.4f}, RMSE {m["rmse"]:.4f}. 운영 입력에는 Target이 없으므로 운영 MAE를 계산하지 않습니다.\n'
            '다음 날 Target의 시점 누출 방지를 위해 Train/Validation 경계 마지막 행은 각 학습 구간에서 제외했습니다.\n'
            '스테이징 디렉터리 생성 후 결과 폴더를 교체합니다. 교체 실패 시 이전 폴더를 되돌리며, 실행 도중 비정상 종료가 발생하는 경우 디렉터리 스냅샷 기반 복구가 추가로 필요합니다.\n',encoding='utf-8')
    atomic_bundle('results',build)


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:raise SystemExit(f'ERROR: {error}') from error
