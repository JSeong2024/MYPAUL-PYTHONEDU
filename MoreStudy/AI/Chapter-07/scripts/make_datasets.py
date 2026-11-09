"""Chapter 07 실습용 합성 데이터 재생성. 외부 네트워크 사용 없음."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data'


def generate(output_dir: Path = OUT) -> dict[str, int]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(1707)
    n = 360
    hours = np.arange(n) % 24
    weekend = (np.arange(n) // 24) % 7 >= 5
    temp = 18 + 7 * np.sin(np.arange(n) * 2 * np.pi / 160) + rng.normal(0, 2, n)
    occupancy = np.clip(70 + 25*np.sin((hours-7)*np.pi/12) - 18*weekend + rng.normal(0, 7, n), 2, 130)
    energy = (8 + .12*temp + .034*occupancy + .021*(temp-22)**2
              + .65*weekend + .65*np.cos(hours*np.pi/12) + rng.normal(0,.55,n))
    energy_df = pd.DataFrame({
        'observation_id':[f'E{i:04d}' for i in range(n)],
        'hour':hours.astype(int),'temperature_c':temp.round(4),'occupancy':occupancy.round(4),
        'is_weekend':weekend.astype(int),'demand_kwh':energy.round(4),
    })
    energy_df.to_csv(output_dir/'energy_demand.csv',index=False)

    n = 420
    vib = rng.normal(3.5, 1.15, n)
    temperature = rng.normal(48, 9, n)
    load = rng.uniform(.2,1,n)
    days = rng.integers(1,160,n)
    logit = (-2.2 + .66*(vib-3.5) + .05*(temperature-48)
             + 1.7*(load-.6) + .009*(days-65) + .24*(vib-3.5)*(load-.6))
    prob=1/(1+np.exp(-logit))
    label=(rng.random(n)<prob).astype(int)
    alerts_df = pd.DataFrame({
        'event_id':[f'A{i:04d}' for i in range(n)],
        'vibration':vib.round(5),'temperature_c':temperature.round(5),
        'load_factor':load.round(5),'days_since_service':days,
        'alert_label':label,
    })
    alerts_df.to_csv(output_dir/'device_alerts.csv',index=False)

    rows=[]
    for site_index in range(6):
        for device_index in range(16):
            dtype=device_index%2
            for week in range(1,9):
                vib = rng.normal(3.0+.36*dtype+.12*site_index, .75)
                temp = rng.normal(51+2.1*dtype+.6*site_index, 6)
                util = rng.uniform(.22,.99)
                days = int(rng.integers(1,181))
                prior=int(rng.poisson(.8+util))
                risk=(-3.0 + .72*(vib-3.0)+.065*(temp-51)
                      +2.1*(util-.55)+.008*(days-75)+.36*prior+.12*dtype
                      +.08*(site_index-2))
                p=1/(1+np.exp(-risk))
                outcome=int(rng.random()<p)
                # 예측 이후에만 알려지는 값을 포함해 Leakage 점검에 사용.
                post=int(outcome if rng.random()<.97 else 1-outcome)
                rows.append((f'F{len(rows):05d}',f'S{site_index+1:02d}',
                    f'S{site_index+1:02d}-D{device_index+1:02d}',week,dtype,
                    round(vib,5),round(temp,5),round(util,5),days,prior,post,outcome))
    fleet_df = pd.DataFrame(rows,columns=[
        'event_id','site_id','device_id','week','equipment_type','vibration',
        'temperature_c','utilization','days_since_service','prior_alerts',
        'post_inspection_result','maintenance_label'])
    fleet_df.to_csv(output_dir/'fleet_events.csv',index=False)
    return {'energy_demand.csv':len(energy_df),'device_alerts.csv':len(alerts_df),
            'fleet_events.csv':len(fleet_df)}

if __name__=='__main__':
    for name,n in generate().items():
        print(f'{name}: {n} rows')
