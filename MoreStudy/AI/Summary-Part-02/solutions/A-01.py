"""A-01: sensor row validation and vectorized calibration."""
import csv, json, sys
from pathlib import Path
import pandas as pd
import torch
from common import args_or_default,finite_number,write_json
FEATURES=['temperature','humidity','power_kw']
def main(argv=None):
 a=args_or_default(argv,'A-01');columns=['record_id','room_id']+FEATURES
 try:
  with (a.data/'sensor_readings.csv').open(newline='',encoding='utf-8-sig') as f:
   reader=csv.DictReader(f)
   if not set(columns).issubset(reader.fieldnames or []):raise ValueError('missing sensor columns')
   data=list(reader)
  with (a.data/'calibration.csv').open(newline='',encoding='utf-8-sig') as f:
   reader=csv.DictReader(f)
   if not {'feature','offset','scale'}.issubset(reader.fieldnames or []):raise ValueError('missing calibration columns')
   calib={}
   for r in reader:
    name=r['feature'];o=finite_number(r['offset']);s=finite_number(r['scale'])
    if name not in FEATURES or name in calib or o is None or s is None or s<=0:raise ValueError('invalid calibration')
    calib[name]=(o,s)
   if set(calib)!=set(FEATURES):raise ValueError('incomplete calibration')
 except (ValueError, OSError) as exc:
  print('INPUT_ERROR',exc,file=sys.stderr);return 1
 valid=[];rejected=[];seen=set()
 for line,row in enumerate(data,2):
  rid=(row.get('record_id') or '').strip();room=(row.get('room_id') or '').strip()
  vals=[finite_number(row.get(f)) for f in FEATURES]
  if not rid or not room or any(row.get(f) is None or not str(row.get(f)).strip() for f in columns):error='MISSING_VALUE'
  elif any(ch.isspace() for ch in rid):error='INVALID_ID'
  elif any(x is None for x in vals) or not -40<=vals[0]<=100 or not 0<=vals[1]<=100 or vals[2]<0:error='INVALID_NUMBER'
  elif rid in seen:error='DUPLICATE_ID'
  else:error=None
  if error:rejected.append({'source_line':line,'record_id':rid,'error_code':error})
  else:
   seen.add(rid);valid.append({'record_id':rid,'room_id':room,**dict(zip(FEATURES,vals))})
 n=len(valid)
 pd.DataFrame(rejected,columns=['source_line','record_id','error_code']).to_csv(a.out/'rejected_rows.csv',index=False)
 mean=None
 if n:
  values=torch.tensor([[v[f] for f in FEATURES] for v in valid],dtype=torch.float32)
  offset=torch.tensor([calib[f][0] for f in FEATURES]);scale=torch.tensor([calib[f][1] for f in FEATURES]);corrected=(values+offset)*scale
  mean=corrected.mean(dim=0).tolist()
  if n>=5:
   out=[{'record_id':v['record_id'],'room_id':v['room_id'],**{f:f'{float(x):.4f}' for f,x in zip(FEATURES,corrected[i].tolist())}} for i,v in enumerate(valid)]
   pd.DataFrame(out,columns=columns).to_csv(a.out/'calibrated.csv',index=False)
 if n<5:(a.out/'calibrated.csv').unlink(missing_ok=True)
 write_json(a.out/'quality_report.json',{'status':'OK' if n>=5 else 'INSUFFICIENT_DATA','valid_count':n,'rejected_count':len(rejected),'shape':[n,3],'channel_mean':mean,'missing_count':max(0,5-n)})
 return 0 if n>=5 else 2
if __name__=='__main__':sys.exit(main())
