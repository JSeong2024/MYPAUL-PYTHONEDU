"""P-03: cluster repeated workspace usage and test seed stability."""
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from common import read_csv, finite, date_str, save_csv

FEATURES=['weekly_bookings','avg_session_min','evening_ratio','cancel_ratio']


def main():
    raw=read_csv('workspace_usage.csv',['room_id','week_start',*FEATURES]); rows=[];rejections=[];seen=set()
    for idx,r in raw.iterrows():
        k=(str(r['room_id']),str(r['week_start']))
        v={c:finite(r[c]) for c in FEATURES}
        reason=None
        if not k[0] or date_str(k[1]) is None:reason='INVALID_ID_OR_DATE'
        elif any(x is None or x<0 for x in v.values()) or any(v[c]>1 for c in ['evening_ratio','cancel_ratio']):reason='INVALID_VALUE'
        elif k in seen:reason='DUPLICATE_RECORD'
        if reason:rejections.append((idx+2,reason));continue
        seen.add(k);rows.append({'room_id':k[0],'week_start':k[1],**v})
    df=pd.DataFrame(rows,columns=['room_id','week_start',*FEATURES])
    if len(df)<50 or len(df[FEATURES].drop_duplicates())<3:raise ValueError('at least 50 valid samples and 3 distinct vectors required')
    X=StandardScaler().fit_transform(df[FEATURES]);labels={s:KMeans(n_clusters=3,n_init=10,random_state=s).fit_predict(X) for s in (7,21,42)}
    save_csv('cluster_assignments.csv',df[['room_id','week_start']].assign(cluster_id=labels[42]))
    profiles=[]
    d=df.copy();d['cluster_id']=labels[42]
    for k,g in d.groupby('cluster_id',sort=True):
        p={'cluster_id':int(k),'sample_count':len(g)}
        p.update({f'mean_{c}':f'{g[c].mean():.4f}' for c in FEATURES});profiles.append(p)
    save_csv('cluster_profiles.csv',profiles,['cluster_id','sample_count',*(f'mean_{c}' for c in FEATURES)])
    stabilities=[{'seed_a':a,'seed_b':b,'ari':f'{adjusted_rand_score(labels[a],labels[b]):.4f}'} for a,b in combinations((7,21,42),2)]
    save_csv('stability.csv',stabilities,['seed_a','seed_b','ari'])
    # Suggestions are tied to measured properties, never to the numeric cluster name itself.
    high_even=max(profiles,key=lambda p:float(p['mean_evening_ratio']))
    high_cancel=max(profiles,key=lambda p:float(p['mean_cancel_ratio']))
    high_booking=max(profiles,key=lambda p:float(p['mean_weekly_bookings']))
    lines=['# 공유 오피스 운영 패턴 검토','',f'정제 제외: {len(rejections)}건. 유효 기록: {len(df)}건.','',
           '## 실행별 안정성','']+[f'- seed {r["seed_a"]} vs {r["seed_b"]}: ARI {r["ari"]}' for r in stabilities]
    lines += ['', '## 공간별 배정 분포']
    for room,g in d.groupby('room_id',sort=True):
        lines.append(f'- {room}: '+', '.join(f'Cluster {int(k)} {int(n)}건' for k,n in g.cluster_id.value_counts().sort_index().items()))
    lines += ['','## 운영 변경안',
             f'1. Cluster {high_even["cluster_id"]}의 저녁 예약 비율 평균은 {high_even["mean_evening_ratio"]}입니다. 저녁 시간 운영 인력을 시험적으로 조정하고 이용률과 인건비를 비교합니다.',
             f'2. Cluster {high_cancel["cluster_id"]}의 취소 비율 평균은 {high_cancel["mean_cancel_ratio"]}입니다. 예약 확인 알림을 시범 도입하고 취소율과 노쇼율을 측정합니다.',
             f'3. Cluster {high_booking["cluster_id"]}의 주간 예약 평균은 {high_booking["mean_weekly_bookings"]}입니다. 혼잡 시간대에 공간 공유를 확대하고 대기 시간을 측정합니다.',
             '','동일 room_id가 주차별로 다른 Cluster에 배정될 수 있습니다. Cluster ID는 고정 등급이 아니며, 높은 ARI도 미래 데이터에 대한 안정성을 보증하지 않습니다.']
    Path('report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':
    try:main()
    except ValueError as error:raise SystemExit(f'ERROR: {error}') from error
