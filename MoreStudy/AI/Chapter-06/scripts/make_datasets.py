"""Chapter 06 실습용 합성 데이터 생성. 외부 다운로드가 필요하지 않습니다."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'


def create_all():
    DATA.mkdir(exist_ok=True)
    rng = np.random.default_rng(42)
    # XOR: 네 구역에 균등한 샘플을 배치. 각 구역의 Label은 부호가 다르면 1.
    rows=[]
    for xsign in (-1,1):
        for ysign in (-1,1):
            for i in range(64):
                x=xsign*(1.0+rng.normal(0,0.24))
                y=ysign*(1.0+rng.normal(0,0.24))
                rows.append((f'X{len(rows)+1:03d}', x, y, int(xsign != ysign)))
    df=pd.DataFrame(rows,columns=['sample_id','signal_x','signal_y','label'])
    df=df.iloc[rng.permutation(len(df))].reset_index(drop=True)
    df.to_csv(DATA/'xor_signals.csv',index=False,float_format='%.6f')
    # 비선형 연속 타깃: 곡면 관계를 갖는 합성 데이터.
    n=300
    temp=rng.uniform(-1.6,1.6,size=n)
    load=rng.uniform(-1.5,1.5,size=n)
    demand=1.5+0.9*np.sin(2.2*temp)+0.7*load**2+0.16*rng.standard_normal(n)
    df=pd.DataFrame({'record_id':[f'D{i:03d}' for i in range(n)],'temperature_scaled':temp,'load_scaled':load,'demand':demand})
    df.to_csv(DATA/'nonlinear_demand.csv',index=False,float_format='%.6f')
    # 3-class: 반복 관측 신호 6개, 비선형 Decision Boundary.
    points=rng.normal(0,1,size=(360,6))
    z1=points[:,0]*points[:,1]+0.7*points[:,2]
    z2=(points[:,3]**2-0.4*points[:,4])+0.4*points[:,5]
    # 클래스가 극단적으로 불균형하지 않게 분위수로 3등분.
    score=z1+z2
    q1,q2=np.quantile(score,[1/3,2/3])
    labels=np.digitize(score,[q1,q2])
    columns={f'f{i+1}':points[:,i] for i in range(6)}
    df=pd.DataFrame({'event_id':[f'E{i:03d}' for i in range(360)],**columns,'class_id':labels})
    df.to_csv(DATA/'triage_signals.csv',index=False,float_format='%.6f')
    # 재현 가능한 분리/가중치 저장을 학생 코드가 직접 수행하게 둡니다.

if __name__=='__main__':
    create_all()
    for f in sorted(DATA.glob('*.csv')): print(f.name, len(pd.read_csv(f)))
