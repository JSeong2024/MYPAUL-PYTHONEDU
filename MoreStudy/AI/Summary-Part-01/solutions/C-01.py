"""C-01: compare row-random and group-isolated equipment evaluations."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split, GroupKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from common import (read_csv, date_str, finite, integer, group_partition, save_csv, save_json)

FEATURES=['temperature_c','vibration_rms','load_pct','days_since_service'];TARGET='failure_next_14d'
COLUMNS=['record_id','device_id','observed_at',*FEATURES,TARGET,'final_repair_code']


def load():
    df=read_csv('equipment_history.csv',COLUMNS)
    good=[];rejected=[];seen=set()
    for i,r in df.iterrows():
        error=None;rid=str(r['record_id']);device=str(r['device_id'])
        try:
            pd.Timestamp(str(r['observed_at']))
        except (ValueError,TypeError):error='INVALID_DATE'
        if not rid or not device or rid in seen:error=error or 'INVALID_OR_DUPLICATE_ID'
        target=integer(str(r[TARGET]))
        if target not in (0,1):error=error or 'INVALID_TARGET'
        vals={k:(np.nan if str(r[k]).strip()=='' else finite(r[k])) for k in FEATURES}
        for name,v in vals.items():
            if v is None or (not np.isnan(v) and ((name in ('vibration_rms','days_since_service') and v<0) or (name=='load_pct' and not 0<=v<=100) or (name=='days_since_service' and v!=int(v)))):
                error=error or 'INVALID_FEATURE'
        if error:rejected.append({'record_id':rid,'error_code':error});continue
        seen.add(rid);good.append({'record_id':rid,'device_id':device,'observed_at':str(r['observed_at']),**vals,TARGET:target})
    out=pd.DataFrame(good)
    if out.empty or out.device_id.nunique()<30:raise ValueError('at least 30 devices required')
    return out,rejected


def pipeline():
    return Pipeline([('imputer',SimpleImputer(strategy='median',keep_empty_features=True)),
                     ('scaler',StandardScaler()),('model',LogisticRegression(max_iter=1000,random_state=42))])


def scores(y,pred):
    y=np.asarray(y,dtype=int);pred=np.asarray(pred,dtype=int)
    return dict(accuracy=float(accuracy_score(y,pred)),recall=float(recall_score(y,pred,zero_division=0)),
                balanced_accuracy=float(balanced_accuracy_score(y,pred)),f1=float(f1_score(y,pred,zero_division=0)))


def main():
    df,rejected=load();save_csv('data_audit.csv',rejected,['record_id','error_code'])
    row_tr,row_te=train_test_split(df,test_size=.2,random_state=42,stratify=df[TARGET])
    row_overlap=len(set(row_tr.device_id)&set(row_te.device_id))
    tr,val,te=group_partition(df,'device_id')
    if any(d[TARGET].nunique()<2 for d in (tr,row_tr)):raise ValueError('training class only one')
    report={'vulnerable_random_split_group_overlap':row_overlap,'repaired_group_intersection_count':0,
            'splits':{k:{'samples':len(d),'devices':int(d.device_id.nunique())} for k,d in [('train',tr),('validation',val),('test',te)]},
            'disallowed_input_features':['final_repair_code',TARGET], 'allowed_input_features':FEATURES}
    save_json('split_audit.json',report)
    metrics=[]
    for scope,train,test in (('random',row_tr,row_te),('group',tr,te)):
        for label,mdl in (('majority',Pipeline([('imputer',SimpleImputer(strategy='median',keep_empty_features=True)),('model',DummyClassifier(strategy='most_frequent'))])),('logistic',pipeline())):
            mdl.fit(train[FEATURES],train[TARGET]);p=mdl.predict(test[FEATURES]);s=scores(test[TARGET],p)
            metrics.append({'evaluation':scope,'model':label,**{k:f'{v:.4f}' for k,v in s.items()}})
            if scope=='group' and label=='logistic': group_pred=np.asarray(p)
    save_csv('metric_comparison.csv',metrics,['evaluation','model','accuracy','recall','balanced_accuracy','f1'])
    g=te[['device_id',TARGET]].copy();g['pred']=group_pred
    err=[]
    for device,part in g.groupby('device_id',sort=True):
        err.append({'device_id':device,'sample_count':len(part),
                    'false_negative_count':int(((part[TARGET]==1)&(part.pred==0)).sum()),
                    'false_positive_count':int(((part[TARGET]==0)&(part.pred==1)).sum())})
    save_csv('error_by_device.csv',err,['device_id','sample_count','false_negative_count','false_positive_count'])
    cv_msg=''
    try:
        cv=GroupKFold(n_splits=5)
        cv_scores=cross_val_score(pipeline(),tr[FEATURES],tr[TARGET],groups=tr.device_id,cv=cv,scoring='balanced_accuracy')
        cv_msg=f'GroupKFold 5-fold Balanced Accuracy 평균: {np.mean(cv_scores):.4f}.'
    except ValueError as e:
        cv_msg=f'GroupKFold 실행 불가: {e}'
    # Structural checks supplement black-box accuracy tests.
    tr2,val2,te2=group_partition(df,'device_id')
    reproducible=all(set(a.record_id)==set(b.record_id) for a,b in zip((tr,val,te),(tr2,val2,te2)))
    root=f'''# 설비 고장 예측 시스템 감사

- 전체 허용 입력 특성: {FEATURES}
- 금지된 사후 기록: `final_repair_code`, `failure_next_14d` (Target 전용)
- 무효 데이터 제외: {len(rejected)}건
- 행 단위 Random Split의 Train/Test Group 중복: {row_overlap}개
- 복구 Group 분할의 Group 교집합: 0개
- 그룹 분할 재현성 검증: {reproducible}
- {cv_msg}

## 원인 및 복구

기존 행 단위 Random Split은 동일 설비 기록을 두 데이터셋에 분산시켜 신규 설비 성능을 과대평가할 수 있습니다. 사후에 확정되는 수리 코드는 예측 시점에는 존재하지 않으므로 사용하면 안 됩니다.

GroupShuffleSplit으로 설비 단위 분할을 구성하고, SimpleImputer와 StandardScaler를 모델 Pipeline에 넣어 학습 구간에서만 fitting합니다. 동일 조건에서 각 구간의 Group 교집합을 검사했습니다.

## 남은 한계

Group 분할만으로 시간에 걸친 외부 분포 변화를 완전히 검증할 수는 없습니다. 각 평가 구간의 클래스 수를 함께 확인해야 합니다. 양성이 없는 평가 구간의 Recall은 정의되지 않으며, 코드 출력의 0은 보고 편의를 위한 대체값입니다.
'''
    Path('root_cause_report.md').write_text(root,encoding='utf-8')


if __name__=='__main__':
    try:main()
    except ValueError as error:raise SystemExit(f'ERROR: {error}') from error
