"""Create deterministic synthetic data for the AI Summary Part 01 exercises.

Usage: python tests/generate_data.py --output data
No downloaded datasets or personal information are used.
"""
from __future__ import annotations
import argparse
from datetime import date,timedelta
from pathlib import Path
import csv
import math
import numpy as np


def write(base, pid, filename, header, rows):
    path=base/pid;path.mkdir(parents=True,exist_ok=True)
    with (path/filename).open('w',encoding='utf-8',newline='') as out:
        writer=csv.writer(out,lineterminator='\n');writer.writerow(header);writer.writerows(rows)


def generate(base):
    rng=np.random.default_rng(2026)
    write(base,'A-01','validation_scores.csv',['record_id','actual','score'],[
        ('R01',0,.2),('R02',1,.65),('R03',1,.48),('R04',0,.70),('R05',1,.74),('R06',0,.15)])
    write(base,'A-01','test_scores.csv',['record_id','actual','score'],[
        ('T01',1,.8),('T02',0,.2),('T03',1,.45),('T04',0,.62),('T05',1,.5),('T06',0,.3)])
    water=[]
    for i in range(50):
        dt=date(2026,4,1)+timedelta(days=i);t=12+i*.18+3*math.sin(i/5)
        occ=int(30+12*math.sin(i*.34)+i%7)
        weekend=int(dt.weekday()>=5); target=5+.55*occ+.9*t-2*weekend+rng.normal(0,1.7)
        water.append((dt.isoformat(),f'{t:.2f}',occ,weekend,f'{target:.3f}'))
    write(base,'A-02','daily_water.csv',['date','temperature_c','occupants','is_weekend','consumption_m3'],water)
    space=[]
    for cluster in range(3):
        for j in range(23):
            vi=max(0,int(rng.normal([2,5,9][cluster],.9)))
            minutes=max(0.,rng.normal([140,75,30][cluster],9))
            ratio=float(np.clip(rng.normal([.15,.52,.86][cluster],.07),0,1))
            space.append((f'S{cluster*23+j+1:03d}',vi,f'{minutes:.2f}',f'{ratio:.4f}'))
    space.append(('BAD',-1,44,.5));space.append(('S001',4,30,.4))
    write(base,'A-03','space_usage.csv',['record_id','weekly_visits','avg_minutes','evening_ratio'],space)
    past=[]
    for unit in range(75):
        for t in range(3):
            age=int(unit%48+12+t);alarms=int(rng.poisson(1.4+unit%6*.4));prior=t
            p=1/(1+math.exp(-(-2+.035*age+.38*alarms+.2*prior)))
            y=int(rng.random()<p)
            past.append((f'C{unit:03d}_{t}',(date(2026,5,1)+timedelta(days=unit+t)).isoformat(),f'U{unit:03d}',age,alarms,prior,y,320*y))
    past.append(('BAD', '2026-06-01','U999',-1,0,0,1,0))
    write(base,'P-01','historical_claims.csv',['claim_id','received_date','unit_id','age_months','alarm_count_30d','prior_claim_count','confirmed_failure','final_repair_cost'],past)
    incoming=[]
    for i in range(23):incoming.append((f'IN{i:03d}',(date(2026,10,12)+timedelta(days=i//9)).isoformat(),f'U{i:03d}',int(i+15),i%8,i%3))
    incoming.append(('BAD','2026-10-12','U050',-2,0,0))
    write(base,'P-01','incoming_claims.csv',['claim_id','received_date','unit_id','age_months','alarm_count_30d','prior_claim_count'],incoming)
    waste=[]
    previous_week={z:float(300+z*87) for z in range(8)}
    for week in range(30):
        week_date=(date(2026,1,5)+timedelta(days=7*week)).isoformat()
        for z in range(8):
            last=previous_week[z]
            events=(week+z)%4; holidays=int(week%7==0)
            nxt=max(0.,round(last+10*events-7*holidays+math.cos(week*.36+z)*12,3))
            waste.append((f'Z{z+1:02d}',week_date,f'{last:.3f}',events,holidays,f'{nxt:.3f}'))
            previous_week[z]=nxt
    waste.append(('Z01','2026-01-05','-4',1,0,20))
    write(base,'P-02','weekly_waste.csv',['zone_id','forecast_week','last_week_kg','planned_events','holiday_days','next_week_kg'],waste)
    work=[]
    for week in range(11):
        for room in range(12):
            category=room%3
            bookings=max(0.,rng.normal([4,17,10][category],1.2))
            minutes=max(0.,rng.normal([180,55,95][category],12))
            evening=float(np.clip(rng.normal([.12,.79,.43][category],.05),0,1))
            cancel=float(np.clip(rng.normal([.12,.06,.31][category],.04),0,1))
            work.append((f'M{room+1:02d}',(date(2026,9,7)+timedelta(days=7*week)).isoformat(),f'{bookings:.2f}',f'{minutes:.2f}',f'{evening:.4f}',f'{cancel:.4f}'))
    work.append(('M01','2026-09-07',22,44,.42,.12))
    write(base,'P-03','workspace_usage.csv',['room_id','week_start','weekly_bookings','avg_session_min','evening_ratio','cancel_ratio'],work)
    equip=[]
    for device in range(45):
        bias=rng.normal(0,1)
        for t in range(9):
            temp=float(36+device%8+2*bias+rng.normal(0,3));vibration=float(max(0,.8+.25*bias+rng.normal(0,.25)))
            load=float(np.clip(50+device%7*4+rng.normal(0,11),0,100));days=int(2+t*4)
            p=1/(1+math.exp(-(-2+.055*(temp-39)+1.6*vibration+.007*load)))
            failure=int(rng.random()<p)
            equip.append((f'ER{device:03d}_{t}',f'D{device:03d}',(date(2026,1,1)+timedelta(days=t*3)).isoformat(),'' if t==2 else f'{temp:.3f}',f'{vibration:.4f}',f'{load:.2f}',days,failure,('REPAIR' if failure else 'NONE')))
    equip.append(('ERR','D100','2026-01-01','33','1.4','130','1','0',''))
    write(base,'C-01','equipment_history.csv',['record_id','device_id','observed_at','temperature_c','vibration_rms','load_pct','days_since_service','failure_next_14d','final_repair_code'],equip)
    library=[]
    for d in range(155):
        day=date(2026,1,1)+timedelta(days=d)
        temp=17+12*math.sin(d/35);e=d%4;w=int(day.weekday()>=5)
        visits=max(0,int(110+3*temp+14*e-18*w+rng.normal(0,6)))
        library.append((day.isoformat(),f'{temp:.3f}',e,w,visits))
    write(base,'C-02','history_v1.csv',['date','temperature_c','scheduled_events','is_weekend','visitors_next_day'],library)
    write(base,'C-02','incoming_v2.csv',['date','temperature_f','scheduled_events','is_weekend'],[
        ('2026-10-01',77,1,0),('2026-10-02','',0,0),('2026-10-01',80,1,0),('2026-10-03',68,0,1)])
    facilities=[(f'F{i:02d}',('NORTH','SOUTH','EAST')[i%3],160+i*21) for i in range(1,16)]
    write(base,'R-01','facilities.csv',['facility_id','district','capacity'],facilities)
    hist=[]
    visitors_by_day={}
    for d in range(181):
        for i,(_,district,cap) in enumerate(facilities,1):
            visitors_by_day[d,i]=max(0,int(cap*.42+16*math.sin(d/9+i)+rng.normal(0,13)))
    for d in range(181):
        day=date(2026,1,1)+timedelta(days=d)
        for i,(_,district,cap) in enumerate(facilities,1):
            visitors=visitors_by_day[d,i]
            energy=max(0,visitors*.36+8+rng.normal(0,2))
            temperature=8+17*math.sin(d/48)
            alarms=int(rng.poisson(.3+i%4*.23))
            p=1/(1+math.exp(-(-3+alarms*.85+.007*visitors)))
            failure=int(rng.random()<p)
            next_vis=visitors_by_day[d+1,i] if d<180 else int(cap*.47)
            hist.append((f'F{i:02d}',day.isoformat(),visitors,f'{energy:.3f}',f'{temperature:.3f}',alarms,failure,next_vis,900 if failure else 0))
    hist.append(hist[0]);hist.append(('F02','2026-01-01',-1,40,18,1,1,100,0))
    write(base,'R-01','daily_operations.csv',['facility_id','date','visitors','energy_kwh','temperature_c','alarms_7d','failure_next_7d','visitors_next_day','final_repair_cost'],hist)
    ops=[]
    for i,(_,district,cap) in enumerate(facilities,1):
        ops.append((f'F{i:02d}','2026-07-01',int(cap*.47),f'{cap*.19:.2f}',23,i%4))
    ops.append(ops[0]); ops.append(('UNREGISTERED','2026-07-01',40,20,22,1))
    write(base,'R-01','incoming_operations.csv',['facility_id','date','visitors','energy_kwh','temperature_c','alarms_7d'],ops)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='data')
    args=parser.parse_args();generate(Path(args.output));print(f'Generated synthetic fixtures at {args.output}')
