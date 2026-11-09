"""Generate deterministic synthetic examples for Summary Part 02."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
rng = np.random.default_rng(42)

def save(name, records):
    path=DATA/name
    path.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame.from_records(records).to_csv(path, index=False, float_format='%.8f')

# A-01: 14 valid, several distinct rejection reasons
records=[]
for i in range(14):
    records.append(dict(record_id=f'R{i+1:03d}', room_id=f'LAB-{i%4+1}',temperature=17+i*.8, humidity=42+i, power_kw=2+i*.12))
records += [dict(record_id='X15',room_id='LAB-1',temperature='',humidity=80,power_kw=2),dict(record_id='R001',room_id='LAB-2',temperature=25,humidity=44,power_kw=3),dict(record_id='X17',room_id='LAB-2',temperature=120,humidity=60,power_kw=3)]
save('sensor_readings.csv',records)
save('calibration.csv',[{'feature':f,'offset':o,'scale':s} for f,o,s in [('temperature',1,1),('humidity',-5,1),('power_kw',0,2)]])

# Reusable synthetic classification and regression datasets
def split_for(i, n):
    return 'train' if i < round(n*.6) else 'validation' if i < round(n*.8) else 'test'

n=220
x=rng.normal(size=(n,2));y=((x[:,0]*x[:,1]+.2*x[:,0]-.12*x[:,1])>0).astype(int)
save('usage.csv',[dict(record_id=f'U{i+1:04d}',split=split_for(i,n),x1=x[i,0],x2=x[i,1],crowded=int(y[i])) for i in range(n)])

n=230
occupancy=rng.uniform(15,95,size=n); temp=rng.uniform(12,34,size=n);weekend=rng.integers(0,2,n)
energy=27+1.36*occupancy+1.8*np.abs(temp-22)+13*weekend+rng.normal(0,2,n)
save('energy.csv',[dict(record_id=f'E{i+1:04d}',split=split_for(i,n),occupancy=occupancy[i],temperature_c=temp[i],weekend=weekend[i],energy_kwh=energy[i]) for i in range(n)])

n=210
temp=rng.uniform(17,55,n);vib=rng.uniform(.5,11,n);hours=rng.uniform(80,750,n)
logits=.14*(temp-34)+.48*(vib-5)+.002*(hours-350)
y=rng.binomial(1,1/(1+np.exp(-logits)))
save('training.csv',[dict(record_id=f'T{i+1:04d}',split=split_for(i,n),temperature_c=temp[i],vibration=vib[i],hours_active=hours[i],needs_service=int(y[i])) for i in range(n)])
save('incoming.csv',[dict(record_id=f'N{i+1:03d}',hours_active=180+10*i,temperature_c=28+i, vibration=2+.22*i) for i in range(40)])

# P-01: group-specific equipment risk; 18 sites * 32 rows
rows=[]
for site in range(18):
 for k in range(32):
    t=rng.uniform(25,68);v=rng.uniform(.5,14);alarm=int(rng.integers(0,12));hours=rng.uniform(150,1800)
    z=-5.1+.055*t+.14*v+.23*alarm+.0006*hours+rng.normal(0,.5)
    label=int(rng.random()<1/(1+np.exp(-z)))
    rows.append(dict(record_id=f'M{site:02d}{k:03d}',site_id=f'S{site+1:02d}',asset_id=f'A{k%17:03d}',recorded_date=f'2026-03-{(k%28)+1:02d}',temperature_c=t,vibration_mm_s=v,alarm_count_7d=alarm,operating_hours=hours,failure_next_7d=label,final_repair_cost=(120000+int(50000*rng.random())) if label else 0))
save('maintenance_history.csv',rows)
rows=[]
for i in range(75):
  site=i%5
  rows.append(dict(record_id=f'IN{i+1:04d}',site_id=f'S{site+19:02d}',asset_id=f'E{i%13:03d}',recorded_date=f'2026-06-{(i%26)+1:02d}',temperature_c=28+i%18,vibration_mm_s=2+i%6,alarm_count_7d=i%8,operating_hours=500+i*7))
save('incoming_maintenance.csv',rows)

# P-02: continuous dates, next-day target, no future features
rows=[]
start=pd.Timestamp('2026-01-01')
for d in range(78):
 date=start+pd.Timedelta(days=d)
 for g in range(6):
    base=80+g*9+12*np.sin(d/6)+rng.normal(0,1.0)
    val=max(0,base)
    nextval=max(0,80+g*9+12*np.sin((d+1)/6)+rng.normal(0,1.1))
    rows.append(dict(grid_id=f'G{g+1:02d}',date=date.strftime('%Y-%m-%d'),energy_kwh=val,temperature_c=8+8*np.sin(d/25),weekday=int(date.weekday()),holiday=int(date.weekday()>=5),alarm_count=int(rng.integers(0,4)),next_day_energy_kwh=nextval))
save('microgrid_daily.csv',rows)

n=236
x=rng.normal(size=(n,4)); z=1.3*x[:,0]-.7*x[:,1]+.9*np.sin(x[:,2])+0.4*x[:,3]
y=rng.binomial(1,1/(1+np.exp(-z)))
save('quality_train.csv',[dict(record_id=f'Q{i+1:04d}',split=split_for(i,n),f1=x[i,0],f2=12+3*x[i,1],f3=2+x[i,2],f4=5+x[i,3],defective=int(y[i])) for i in range(n)])

n=180
x=rng.normal(size=(n,4)); z=.9*x[:,0]-x[:,1]+.6*x[:,2]+.25*x[:,3]
y=rng.binomial(1,1/(1+np.exp(-z)))
trainrows=[dict(record_id=f'C{i+1:03d}',f1=x[i,0],f2=x[i,1],f3=x[i,2],f4=x[i,3],label=int(y[i])) for i in range(n)]
save('train.csv',trainrows[:135]);save('validation.csv',trainrows[135:])

# C-02 known-good model and reference cases
from torch import nn
torch.manual_seed(42)
model=nn.Sequential(nn.Linear(3,8),nn.ReLU(),nn.Linear(8,1))
torch.save(model.state_dict(),DATA/'model_weights.pt')
mean=[34.,4.,300.];scale=[8.,2.5,130.]
config={'input_dim':3,'hidden_dim':8,'output_dim':1,'model_version':'v1','activation':'relu'}
(DATA/'model_config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
prep={'feature_order':['temperature_c','vibration','hours_active'],'mean':mean,'scale':scale,'threshold':.5,'training_min':[18.,0.,80.],'training_max':[55.,11.,750.]}
(DATA/'preprocessing.json').write_text(json.dumps(prep,indent=2))
ref=[{'record_id':f'REF{i+1:03d}','temperature_c':22+i*2,'vibration':1+i*.6,'hours_active':120+i*32} for i in range(12)]
with torch.inference_mode():
 inp=torch.tensor([[ (r[f]-m)/sc for f,m,sc in zip(prep['feature_order'],mean,scale)] for r in ref],dtype=torch.float32)
 probs=torch.sigmoid(model(inp)).flatten().tolist()
for r,p in zip(ref,probs):r['probability']=format(p,'.12g')
save('reference_cases.csv',ref)
save('C-02/incoming.csv',[dict(record_id=f'I{i+1:03d}', hours_active=180+10*i,vibration=1+(.22*i),temperature_c=23+i*.55) for i in range(40)]+[dict(record_id='I_INVALID',hours_active=180,vibration='unknown',temperature_c=30)])

# R-01 12 sites; deterministic date ranges; holdouts every fifth site
sites=[dict(site_id=f'S{i+1:03d}',zone=['NORTH','SOUTH','EAST'][i%3],capacity=100+10*i) for i in range(12)]
save('sites.csv',sites)
rows=[]
start=pd.Timestamp('2026-03-01');end=pd.Timestamp('2026-08-11')
for d,date in enumerate(pd.date_range(start,end)):
 for i,s in enumerate(sites):
    temp=18+7*np.sin(d/25)+i*.55;vib=max(0,1.2+i*.24+.2*np.sin(d/7));energy=35+s['capacity']*.34+4*np.cos(d/9)+i*.4
    alarms=int((d+i)%7==0)+int((d+i)%13==0)
    z=-.65+.95*(vib-2.3)+.55*alarms + .045*(temp-20)
    failure=int(rng.random()<1/(1+np.exp(-z)))
    rows.append(dict(site_id=s['site_id'],date=date.strftime('%Y-%m-%d'),temperature_c=temp,vibration=vib,energy_kwh=energy,alarms_7d=alarms,failure_next_7d=failure,energy_next_day=energy+3*np.sin((d+1)/9)+rng.normal(0,1.2),final_repair_cost=100000 if failure else 0))
save('history.csv',rows)
rows=[]
for day in range(3):
 for s in sites:
    rows.append(dict(site_id=s['site_id'],date=(pd.Timestamp('2026-09-01')+pd.Timedelta(days=day)).strftime('%Y-%m-%d'),temperature_c=25, vibration=2.8, energy_kwh=80, alarms_7d=1))
save('R-01/incoming.csv',rows)
(DATA/'deployment_manifest.json').write_text(json.dumps({'active_version':None,'status':'EMPTY'},indent=2))
print('Generated',len(list(DATA.iterdir())),'files')
