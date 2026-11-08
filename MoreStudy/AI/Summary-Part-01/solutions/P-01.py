"""P-01: group-isolated repair triage with daily review capacity."""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from common import (read_csv, integer, finite, date_str, group_partition, metric,
                    save_csv, save_json, valid_record_id)

FEATURES=['age_months','alarm_count_30d','prior_claim_count']
HIST=['claim_id','received_date','unit_id',*FEATURES,'confirmed_failure','final_repair_cost']
INCOMING=['claim_id','received_date','unit_id',*FEATURES]


def validate(name,columns,invalid):
    raw=read_csv(name,columns); rows=[]; seen=set()
    for i,r in raw.iterrows():
        reason=None
        if not all(valid_record_id(str(r[k])) for k in ('claim_id','unit_id')) or date_str(str(r['received_date'])) is None:
            reason='INVALID_IDENTIFIER_OR_DATE'
        ints={k:integer(str(r[k])) for k in FEATURES}
        if any(v is None for v in ints.values()): reason=reason or 'INVALID_FEATURE'
        if 'confirmed_failure' in columns and integer(str(r['confirmed_failure'])) not in (0,1):
            reason=reason or 'INVALID_TARGET'
        if r['claim_id'] in seen:reason=reason or 'DUPLICATE_CLAIM'
        if reason:
            invalid.append({'source_file':name,'source_line':i+2,'error_code':reason})
        else:
            seen.add(str(r['claim_id']))
            row={key:str(r[key]) for key in columns}
            row.update(ints)
            if 'confirmed_failure' in columns:row['confirmed_failure']=integer(str(r['confirmed_failure']))
            rows.append(row)
    return pd.DataFrame(rows,columns=columns)


def main():
    invalid=[]
    hist=validate('historical_claims.csv',HIST,invalid)
    incoming=validate('incoming_claims.csv',INCOMING,invalid)
    save_csv('invalid_claims.csv',invalid,['source_file','source_line','error_code'])
    if hist['unit_id'].nunique()<10:raise ValueError('insufficient distinct units for group split')
    train,val,test=group_partition(hist,'unit_id')
    if train['confirmed_failure'].nunique()<2:raise ValueError('training labels contain only one class')
    baseline=DummyClassifier(strategy='most_frequent').fit(train[FEATURES],train['confirmed_failure'])
    model=Pipeline([('scaler',StandardScaler()),('model',LogisticRegression(max_iter=1000,random_state=42))])
    model.fit(train[FEATURES],train['confirmed_failure'])
    v_scores=model.predict_proba(val[FEATURES])[:,list(model.classes_).index(1)]
    candidates=[.35,.50,.65]; options=[]
    for th in candidates:
        opts=metric(val['confirmed_failure'],(v_scores>=th).astype(int),beta=2)
        options.append({'threshold':th,'f2':opts['f2']})
    winner=max(options,key=lambda x:(x['f2'],x['threshold']))
    th=winner['threshold']
    t_scores=model.predict_proba(test[FEATURES])[:,list(model.classes_).index(1)]
    score=metric(test['confirmed_failure'],(t_scores>=th).astype(int),beta=2)
    baseline_metrics=metric(test['confirmed_failure'],baseline.predict(test[FEATURES]),beta=2)
    split={k:{'samples':len(d),'units':int(d['unit_id'].nunique())} for k,d in [('train',train),('validation',val),('test',test)]}
    result={'splits':split,'group_intersections':0,'threshold_candidates':options,'chosen_threshold':th,
            'test_model_metrics':score,'test_baseline_metrics':baseline_metrics,
            'invalid_claims':len(invalid),'incoming_valid_count':len(incoming)}
    save_json('evaluation.json',result)
    if not incoming.empty:
        incoming=incoming.copy()
        incoming['failure_score']=model.predict_proba(incoming[FEATURES])[:,list(model.classes_).index(1)]
        incoming['decision']='NOT_SELECTED'
        selection=[]
        for date,group in incoming[incoming['failure_score']>=th].groupby('received_date',sort=True):
            ranked=group.sort_values(['failure_score','claim_id'],ascending=[False,True],kind='stable').head(3)
            for rank,(idx,r) in enumerate(ranked.iterrows(),start=1):
                selection.append({'received_date':date,'rank':rank,'claim_id':r['claim_id'],'failure_score':f'{r["failure_score"]:.4f}'})
                incoming.at[idx,'decision']='SELECTED'
    else: selection=[]
    raw=read_csv('incoming_claims.csv',INCOMING)
    decisions={str(r['claim_id']):r['decision'] for _,r in incoming.iterrows()}
    # Invalid input remains represented as NOT_SELECTED; original row count/order is retained.
    save_csv('incoming_decisions.csv',[
        {'claim_id':str(r['claim_id']),'decision':decisions.get(str(r['claim_id']),'NOT_SELECTED')}
        for _,r in raw.iterrows()],['claim_id','decision'])
    save_csv('daily_review_queue.csv',selection,['received_date','rank','claim_id','failure_score'])
    Path('report.md').write_text(
        '# 보증수리 우선순위 분석\n\n'
        '사후 확정되는 confirmed_failure와 final_repair_cost는 모델 입력에 사용하지 않았습니다.\n'
        '제품 단위 GroupShuffleSplit으로 동일 unit_id가 분할을 넘나들지 않도록 했습니다.\n'
        f'Validation F2로 선택한 임계값: {th:.2f}\n\n'
        f'Test Precision {score["precision"]:.4f}, Recall {score["recall"]:.4f}, F2 {score["f2"]:.4f}.\n'
        '이 Test 지표는 임계값 기준 분류 성능이고, 운영 큐의 날짜별 최대 3건 제한이 반영된 지표가 아닙니다.\n'
        f'유효 운영 접수: {len(incoming)}건. 제외 입력은 invalid_claims.csv에 기록했고 NOT_SELECTED로 보존했습니다.\n'
        '검토 인력 한도가 고장 검출률에 미치는 영향은 실제 운영 Target이 수집된 후 별도로 평가해야 합니다.\n',encoding='utf-8')


if __name__=='__main__':
    try:main()
    except ValueError as error:raise SystemExit(f'ERROR: {error}') from error
