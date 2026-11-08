"""R-01: reproducible municipal operations audit and prediction pipeline.

Run in a directory containing facilities.csv, daily_operations.csv and
incoming_operations.csv. Outputs are published together to results/.
"""
from __future__ import annotations
from collections import Counter
from datetime import date,timedelta
from pathlib import Path
from time import perf_counter
import tracemalloc
import platform
import sys
import sklearn

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression,Ridge
from sklearn.metrics import adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from common import (read_csv,integer,finite,date_str,metric,regression_metrics,
                    save_csv,save_json,atomic_bundle)

NUMBERS=['visitors','energy_kwh','temperature_c','alarms_7d']
CLASS_TARGET='failure_next_7d';REG_TARGET='visitors_next_day'
FEATURES=[*NUMBERS,'capacity']
HISTORY=['facility_id','date',*NUMBERS,CLASS_TARGET,REG_TARGET,'final_repair_cost']
INCOMING=['facility_id','date',*NUMBERS]
THRESHOLDS=[.25,.40,.55]; ALPHAS=[.1,1.,10.]


def facilities_table():
    df=read_csv('facilities.csv',['facility_id','district','capacity'])
    if df.empty:raise ValueError('facilities.csv: empty reference table')
    seen=set();data=[]
    for i,r in df.iterrows():
        fid=str(r['facility_id']);district=str(r['district']);capacity=integer(str(r['capacity']),lo=1)
        if not fid or not district or capacity is None or fid in seen:
            raise ValueError(f'facilities.csv: invalid reference row {i+2} or duplicate facility_id')
        seen.add(fid);data.append({'facility_id':fid,'district':district,'capacity':capacity})
    return pd.DataFrame(data).sort_values('facility_id').reset_index(drop=True)


def clean_rows(name, columns, lookup):
    raw=read_csv(name,columns);accepted=[];errors=[];seen=set()
    for i,r in raw.iterrows():
        fid=str(r['facility_id']);day=date_str(str(r['date'])); key=(fid,day)
        reason=None
        if fid not in lookup:reason='UNKNOWN_FACILITY'
        elif day is None:reason='INVALID_NUMBER' # malformed date is also a bad required input
        vals={}
        for k in NUMBERS:
            val=integer(str(r[k])) if k in ('visitors','alarms_7d') else finite(r[k])
            if val is None or (k!='temperature_c' and val<0):reason=reason or 'INVALID_NUMBER'
            vals[k]=val
        if CLASS_TARGET in columns:
            failure=integer(str(r[CLASS_TARGET]));next_day=integer(str(r[REG_TARGET]))
            if failure not in (0,1) or next_day is None:reason=reason or 'INVALID_TARGET'
        if reason is None and key in seen:reason='DUPLICATE_RECORD'
        if reason:
            errors.append({'source_file':name,'source_line':i+2,'error_code':reason})
            continue
        seen.add(key)
        row={'facility_id':fid,'date':day,**vals}
        if CLASS_TARGET in columns:
            row.update({CLASS_TARGET:failure,REG_TARGET:next_day,'final_repair_cost':str(r['final_repair_cost'])})
        accepted.append(row)
    out=pd.DataFrame(accepted,columns=columns)
    if not out.empty:out=out.sort_values(['date','facility_id'],kind='stable').reset_index(drop=True)
    return out,errors


def split_history(df):
    ids=sorted(df.facility_id.unique())
    holdout=set(ids[4::5])
    d=df.copy();d['holdout']=d.facility_id.isin(holdout)
    tr=d[(d.date>='2026-01-01')&(d.date<='2026-04-30')&~d.holdout].copy()
    val=d[(d.date>='2026-05-08')&(d.date<='2026-05-31')&~d.holdout].copy()
    test_a=d[(d.date>='2026-06-08')&(d.date<='2026-06-30')&~d.holdout].copy()
    test_b=d[(d.date>='2026-06-08')&(d.date<='2026-06-30')&d.holdout].copy()
    gap=d[((d.date>='2026-05-01')&(d.date<='2026-05-07'))|
          ((d.date>='2026-06-01')&(d.date<='2026-06-07'))]
    if len(ids)<10 or min(map(len,(tr,val,test_a,test_b)))==0:
        raise ValueError('insufficient facilities or missing training/evaluation periods')
    assert not (set(tr.facility_id)|set(val.facility_id)|set(test_a.facility_id))&holdout
    assert set(test_b.facility_id)<=holdout
    return holdout,tr,val,test_a,test_b,gap


def classifier():
    return Pipeline([('scaler',StandardScaler()),('model',LogisticRegression(max_iter=1000,random_state=42))])


def regressor(alpha):
    return Pipeline([('scaler',StandardScaler()),('model',Ridge(alpha=alpha))])


def rounded_metrics(d):
    return {k:(round(v,4) if isinstance(v,float) else v) for k,v in d.items()}


def evaluate(test, label, model, dummy, ridge, threshold):
    y=test[CLASS_TARGET].to_numpy(dtype=int)
    score=model.predict_proba(test[FEATURES])[:,list(model.classes_).index(1)]
    pred=(score>=threshold).astype(int)
    m=rounded_metrics(metric(y,pred,beta=2))
    bm=rounded_metrics(metric(y,dummy.predict(test[FEATURES]),beta=2))
    actual=test[REG_TARGET].to_numpy(dtype=float)
    estimated=ridge.predict(test[FEATURES]);baseline=test['visitors'].to_numpy(dtype=float)
    reg=rounded_metrics(regression_metrics(actual,estimated))
    reg_base=rounded_metrics(regression_metrics(actual,baseline))
    rows=test[['facility_id','date','district']].copy()
    rows['evaluation']=label;rows['actual_failure']=y;rows['failure_score']=[f'{x:.4f}' for x in score]
    rows['predicted_failure']=pred;rows['actual_visitors']=actual.astype(int)
    rows['predicted_visitors']=[f'{v:.2f}' for v in estimated]
    rows['residual']=[f'{v:.2f}' for v in actual-estimated]
    return rows,dict(classification=m,majority_baseline=bm,regression=reg,persistence_baseline=reg_base)


def profiles_and_predict(train,operational):
    cols=['visitors','energy_kwh','alarms_7d']
    scaler=StandardScaler();x=scaler.fit_transform(train[cols]);
    kmeans=KMeans(n_clusters=3,n_init=10,random_state=42).fit(x)
    cmp=KMeans(n_clusters=3,n_init=10,random_state=7).fit_predict(x)
    labels=kmeans.labels_
    profile=[]; g=train.assign(cluster_id=labels)
    for k,grp in g.groupby('cluster_id',sort=True):
        profile.append({'cluster_id':int(k),'sample_count':len(grp),
                        **{f'mean_{c}':f'{grp[c].mean():.4f}' for c in cols}})
    pred=kmeans.predict(scaler.transform(operational[cols])) if len(operational) else np.array([],dtype=int)
    return profile,pred,float(adjusted_rand_score(labels,cmp))


def inspection_candidates(incoming, scores, threshold):
    df=incoming[['facility_id','date','district']].copy()
    df['failure_score']=scores
    df['inspection_status']='BELOW_THRESHOLD';queue=[]
    for (day,district),g in df[df.failure_score>=threshold].groupby(['date','district'],sort=True):
        ordered=g.sort_values(['failure_score','facility_id'],ascending=[False,True],kind='stable')
        for rank,(idx,row) in enumerate(ordered.iterrows(),start=1):
            if rank<=10:
                df.loc[idx,'inspection_status']='SELECTED'
                queue.append({'date':day,'district':district,'rank':rank,'facility_id':row.facility_id,'failure_score':f'{row.failure_score:.4f}'})
            else:df.loc[idx,'inspection_status']='CAPACITY_LIMIT'
    return df['inspection_status'].tolist(),queue


def benchmark(reference):
    # 100k schema-shaped synthetic rows; isolate reference lookups to compare
    # identical values before/after optimization, without confounding model fitting.
    ids=reference.facility_id.tolist();fields=reference.set_index('facility_id')['capacity'].to_dict()
    n=100_000
    records=[(ids[i%len(ids)],'2026-01-01',i%350,float(i%90),float(i%36-5),i%4) for i in range(n)]
    slow_pairs=list(zip(ids,reference.capacity.tolist()))
    def slow():
        return [next(cap for fid,cap in slow_pairs if fid==item[0]) for item in records]
    def fast():
        return [fields[item[0]] for item in records]
    trials=[]
    for name,fn in [('linear_scan',slow),('dictionary',fast)]:
        tracemalloc.start();t0=perf_counter();out=fn();dt=perf_counter()-t0
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        trials.append({'method':name,'seconds':dt,'peak_bytes':peak,'output':out})
    if trials[0]['output']!=trials[1]['output']:
        raise AssertionError('optimized lookup changed results')
    return trials


def main():
    reference=facilities_table();lookup=reference.set_index('facility_id').to_dict('index')
    hist,err_h=clean_rows('daily_operations.csv',HISTORY,lookup)
    inc,err_i=clean_rows('incoming_operations.csv',INCOMING,lookup)
    if hist.empty or inc.empty:raise ValueError('insufficient valid history or incoming data')
    clean=hist.copy();hist=hist.merge(reference,on='facility_id',how='left',validate='many_to_one')
    inc=inc.merge(reference,on='facility_id',how='left',validate='many_to_one')
    holdout,tr,val,te_a,te_b,gap=split_history(hist)
    if tr[CLASS_TARGET].nunique()<2:raise ValueError('training failure target contains one class only')
    dummy=DummyClassifier(strategy='most_frequent').fit(tr[FEATURES],tr[CLASS_TARGET])
    classification=classifier().fit(tr[FEATURES],tr[CLASS_TARGET])
    vprob=classification.predict_proba(val[FEATURES])[:,list(classification.classes_).index(1)]
    thresholds=[{'threshold':th,'validation_f2':float(metric(val[CLASS_TARGET],(vprob>=th).astype(int),beta=2)['f2'])} for th in THRESHOLDS]
    best_th=max(thresholds,key=lambda x:(x['validation_f2'],x['threshold']))['threshold']
    runs=[]
    for alpha in ALPHAS:
        mdl=regressor(alpha).fit(tr[FEATURES],tr[REG_TARGET]);mae=regression_metrics(val[REG_TARGET],mdl.predict(val[FEATURES]))['mae']
        runs.append((mae,alpha,mdl))
    _,best_alpha,ridge=min(runs,key=lambda x:(x[0],x[1]))
    test_a,eval_a=evaluate(te_a,'A',classification,dummy,ridge,best_th)
    test_b,eval_b=evaluate(te_b,'B',classification,dummy,ridge,best_th)
    test_out=pd.concat([test_a,test_b],ignore_index=True).sort_values(['date','facility_id'])
    iscores=classification.predict_proba(inc[FEATURES])[:,list(classification.classes_).index(1)]
    rpred=ridge.predict(inc[FEATURES]);profiles,clusters,stability=profiles_and_predict(tr,inc)
    selection,queue=inspection_candidates(inc,iscores,best_th)
    operation=inc[['facility_id','date','district']].copy()
    operation['failure_score']=[f'{s:.4f}' for s in iscores]
    operation['predicted_visitors']=[f'{s:.2f}' for s in rpred]
    operation['cluster_id']=clusters;operation['inspection_status']=selection
    regions=[]
    for name,d in [('A',test_a),('B',test_b)]:
        for district,g in d.groupby('district',sort=True):
            regions.append({'evaluation':name,'district':district,'sample_count':len(g),
                            'mae':round(float(np.mean(abs(g.residual.astype(float)))),4)})
    under=test_out.copy();under['residual']=under.residual.astype(float)
    under=under[under.residual>0].sort_values(['residual','date','facility_id'],ascending=[False,True,True]).head(10)
    rejected=err_h+err_i
    splits={'train':{'samples':len(tr),'facilities':int(tr.facility_id.nunique())},
            'validation':{'samples':len(val),'facilities':int(val.facility_id.nunique())},
            'test_A':{'samples':len(te_a),'facilities':int(te_a.facility_id.nunique())},
            'test_B':{'samples':len(te_b),'facilities':int(te_b.facility_id.nunique())},
            'gap_excluded_rows':len(gap),'holdout_facilities':sorted(holdout),'holdout_train_intersection':0,
            'valid_history_rows':len(hist),'valid_incoming_rows':len(inc),'rejected_rows':len(rejected)}
    model_report={'features':FEATURES,'forbidden_features':['final_repair_cost',CLASS_TARGET,REG_TARGET],
                  'threshold_candidates':[{k:round(v,4) for k,v in r.items()} for r in thresholds],
                  'chosen_threshold':best_th,'regression_alpha':best_alpha,
                  'validation_regression_mae_by_alpha':{str(alpha):round(mae,4) for mae,alpha,_ in runs},
                  'evaluation_A':eval_a,'evaluation_B':eval_b,'cluster_ari_seed_42_vs_7':round(stability,4),
                  'regional_regression':regions,'underprediction_top10':under[['facility_id','date','evaluation','residual']].to_dict('records')}
    trials=benchmark(reference)
    perf=('# 처리 효율 분석\n\n'
          '실습용 합성 데이터 100,000건으로 시설 기준 정보 조회 연산을 비교했습니다.\n'
          f'환경: {platform.system()} {platform.machine()}, Python {sys.version.split()[0]}, scikit-learn {sklearn.__version__}.\n'
          '시간과 메모리 측정값은 실행 환경과 부하에 따라 달라집니다. 전체 모델 학습 속도는 포함하지 않습니다.\n\n'
          '| 방식 | 처리 시간(s) | Peak allocation(bytes) |\n|---|---:|---:|\n')
    for entry in trials:
        perf+=f'| {entry["method"]} | {entry["seconds"]:.6f} | {entry["peak_bytes"]} |\n'
    perf+='\n두 구현의 반환 배열이 정확히 동일함을 확인했습니다. 향후에는 실제 CSV 파싱과 모델 추론의 처리량도 별도로 측정할 수 있습니다.\n'
    def build(stage):
        save_csv(stage/'clean_history.csv',clean)
        save_csv(stage/'rejected_rows.csv',rejected,['source_file','source_line','error_code'])
        save_json(stage/'split_report.json',splits)
        save_json(stage/'model_report.json',model_report)
        save_csv(stage/'test_predictions.csv',test_out[['facility_id','date','evaluation','actual_failure','failure_score','predicted_failure','actual_visitors','predicted_visitors','residual']])
        save_csv(stage/'operational_predictions.csv',operation)
        save_csv(stage/'inspection_queue.csv',queue,['date','district','rank','facility_id','failure_score'])
        save_csv(stage/'cluster_profiles.csv',profiles,['cluster_id','sample_count','mean_visitors','mean_energy_kwh','mean_alarms_7d'])
        stage.joinpath('performance_report.md').write_text(perf,encoding='utf-8')
        stage.joinpath('final_report.md').write_text(
            '# 도시 공공시설 통합 운영 분석\n\n'
            f'- 유효 과거 {len(hist)}건, 운영 {len(inc)}건, 거부 {len(rejected)}건. 오류 코드: {dict(Counter(r["error_code"] for r in rejected))}\n'
            f'- 신규 시설 Holdout: {", ".join(sorted(holdout))}; 기존 시설 Test {len(te_a)}건 / 신규 시설 Test {len(te_b)}건.\n'
            '- 고장 이후의 수리비 및 미래 Target은 예측 특성에 포함하지 않았습니다. 7일 Gap으로 인접 기간의 Target 경계 중복을 줄였습니다.\n'
            f'- Classification 임계값 {best_th:.2f}는 기존 시설 Validation F2로 선정했고, 이후 Test A/B 점수는 설정 선택에 쓰지 않았습니다.\n'
            f'- 고장 Test A Recall {eval_a["classification"]["recall"]:.4f}, Test B Recall {eval_b["classification"]["recall"]:.4f}. 두 평가를 합치지 않았습니다.\n'
            f'- Regression alpha {best_alpha:.1f}, Test A MAE {eval_a["regression"]["mae"]:.4f}, Test B MAE {eval_b["regression"]["mae"]:.4f}.\n'
            f'- Clustering 초기화 ARI (42 vs 7): {stability:.4f}. Cluster ID는 실제 시설 등급이 아니며, 시설별 이용 기록 수준의 상대적 구분입니다.\n'
            '- 지역별 MAE는 model_report.json에, 큰 과소 예측 상위 사례도 같은 파일에 정리했습니다.\n'
            '- 운영 점검은 지역·날짜별 최대 10개로 제한하며 Threshold 미달과 정원 초과 사유를 유지합니다.\n'
            '- 모든 결과를 스테이징 디렉터리에서 생성한 후 결과 폴더를 교체합니다. 교체 실패는 롤백하나 비정상 프로세스 종료 시에는 별도 스냅샷이 필요합니다.\n'
            '- 성능 측정은 시설 기준 정보 조회 단계만을 비교했습니다. 성능 보고서의 실행 시간·메모리 측정값은 반복 실행마다 달라질 수 있지만 모델 산출물은 동일해야 합니다.\n'
            '- 모델의 재학습 주기, 실제 장애 신고 확인, 예측 비용 함수의 현장 적합성은 추가 확인이 필요합니다.\n',encoding='utf-8')
    atomic_bundle('results',build)


if __name__=='__main__':
    try: main()
    except (ValueError,OSError,AssertionError) as error:
        raise SystemExit(f'ERROR: {error}') from error
