"""A-03: validate, standardize and profile KMeans/DBSCAN labels."""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from common import read_csv, finite, integer, save_csv, valid_record_id

FEATURES=['weekly_visits','avg_minutes','evening_ratio']


def main():
    df=read_csv('space_usage.csv',['record_id',*FEATURES])
    valid=[]; invalid=[]; seen=set()
    for idx,row in df.iterrows():
        reason=None; rid=str(row['record_id'])
        visits=integer(str(row['weekly_visits']))
        duration=finite(row['avg_minutes']);ratio=finite(row['evening_ratio'])
        if not valid_record_id(rid) or visits is None or duration is None or duration<0 or ratio is None or not 0<=ratio<=1:
            reason='INVALID_VALUE'
        elif rid in seen:
            reason='DUPLICATE_ID'
        if reason:
            invalid.append({'row_number':idx+2,'error_code':reason})
        else:
            seen.add(rid);valid.append({'record_id':rid,'weekly_visits':visits,'avg_minutes':duration,'evening_ratio':ratio})
    save_csv('invalid_rows.csv',invalid,['row_number','error_code'])
    v=pd.DataFrame(valid,columns=['record_id',*FEATURES]);
    if len(v)<30 or len(v[FEATURES].drop_duplicates())<3:
        raise ValueError('insufficient valid/distinct samples for KMeans')
    scaled=StandardScaler().fit_transform(v[FEATURES]); k=KMeans(n_clusters=3,random_state=42,n_init=10).fit_predict(scaled)
    d=DBSCAN(eps=.6,min_samples=5).fit_predict(scaled)
    save_csv('cluster_assignments.csv',pd.DataFrame({'record_id':v['record_id'],'kmeans_cluster':k,'dbscan_cluster':d}))
    profiles=[]
    for method,labels in [('kmeans',k),('dbscan',d)]:
        sub=v.copy();sub['cluster_id']=labels
        for cid,g in sub.groupby('cluster_id',sort=True):
            p={'method':method,'cluster_id':int(cid),'sample_count':len(g)}
            p.update({f'mean_{c}':f'{g[c].mean():.4f}' for c in FEATURES})
            profiles.append(p)
    save_csv('cluster_profiles.csv',profiles,['method','cluster_id','sample_count',*(f'mean_{c}' for c in FEATURES)])
    noise=int(np.sum(d==-1))
    lines=['# 이용 패턴 분석',f'유효 샘플: {len(v)}개 · 제외: {len(invalid)}개 · DBSCAN Noise: {noise}개',
           '', 'KMeans는 3개의 군집을 구성하며 DBSCAN은 밀도 기반으로 Noise를 구분합니다.',
           '각 Cluster ID는 알고리즘에 따라 임의로 붙는 번호이며 두 모델 간 같은 의미를 갖지 않습니다.',
           '군집은 검증된 사용자 유형이나 Ground Truth Label이 아닙니다.','', '## 클러스터별 원본 단위 평균']
    for p in profiles:
        lines.append(f'- {p["method"]} / {p["cluster_id"]}: {p["sample_count"]}건, 방문 {p["mean_weekly_visits"]}회, 체류 {p["mean_avg_minutes"]}분, 저녁 비율 {p["mean_evening_ratio"]}')
    Path('report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':
    try: main()
    except ValueError as error: raise SystemExit(f'ERROR: {error}') from error
