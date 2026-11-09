"""C-02: safe inference audit, reference gate and distribution shift policy."""
import csv,sys,json
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from common import args_or_default,finite_number,make_mlp,write_json
F=['temperature_c','vibration','hours_active']

def read_csv(path,required):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f)
  if not set(required).issubset(reader.fieldnames or []):raise ValueError('SCHEMA_ERROR: '+path.name)
  return list(reader)

def main(argv=None):
 a=args_or_default(argv,'C-02');pre=json.loads((a.data/'preprocessing.json').read_text());config=json.loads((a.data/'model_config.json').read_text())
 manifest={'model_version':config.get('model_version'),'schema_valid':False,'reference_max_abs_diff':None,'valid_count':0,'invalid_count':0,'out_of_range_ratio':None,'shift_alert':False,'automatic_decisions_enabled':False}
 try:
  if pre['feature_order']!=F or config['input_dim']!=3 or config['hidden_dim']!=8 or config['output_dim']!=1:raise ValueError('MODEL_CONFIG_ERROR')
  incoming=read_csv(a.data/'C-02'/'incoming.csv',['record_id']+F)
  reference=read_csv(a.data/'reference_cases.csv',['record_id']+F+['probability'])
  manifest['schema_valid']=True
  model=make_mlp([3,8,1]);model.load_state_dict(torch.load(a.data/'model_weights.pt',map_location='cpu',weights_only=True))
  model.eval()
  def raw_predict(vals):
   x=torch.tensor((np.asarray(vals,dtype='float64')-np.asarray(pre['mean']))/np.asarray(pre['scale']),dtype=torch.float32)
   with torch.inference_mode():return torch.sigmoid(model(x)).flatten().numpy()
  refprob=raw_predict([[float(r[f]) for f in F] for r in reference])
  diff=float(max(abs(refprob[i]-float(r['probability'])) for i,r in enumerate(reference)))
  manifest['reference_max_abs_diff']=diff
  if diff>1e-6:raise ValueError('REFERENCE_MISMATCH')
  accepted=[];errors=[];seen=set()
  for line,r in enumerate(incoming,2):
   rid=(r.get('record_id') or '').strip();vals=[finite_number(r.get(f)) for f in F]
   if not rid or any(v is None for v in vals) or vals[1]<0 or vals[2]<0:code='INVALID_VALUE'
   elif rid in seen:code='DUPLICATE_ID'
   else:code=None
   if code:errors.append({'source_line':line,'record_id':rid,'error_code':code})
   else:seen.add(rid);accepted.append((rid,vals))
  manifest['valid_count']=len(accepted);manifest['invalid_count']=len(errors)
  outof=[any(v<lo or v>hi for v,lo,hi in zip(vals,pre['training_min'],pre['training_max'])) for _,vals in accepted]
  ratio=float(np.mean(outof)) if accepted else 0.
  alert=len(accepted)>=30 and ratio>.2
  manifest['out_of_range_ratio']=ratio;manifest['shift_alert']=alert;manifest['automatic_decisions_enabled']=not alert
  probs=raw_predict([r[1] for r in accepted]) if accepted else np.array([])
  pred=[{'record_id':rid,'probability':f'{p:.6f}','predicted':int(p>=pre['threshold']),'status':'REVIEW_REQUIRED' if alert else 'AUTO'} for (rid,_),p in zip(accepted,probs)]
  # All validation is finished before the published predictions file is replaced.
  path=a.out/'predictions.csv';tmp=a.out/'predictions.csv.tmp'
  pd.DataFrame(pred,columns=['record_id','probability','predicted','status']).to_csv(tmp,index=False)
  tmp.replace(path)
  pd.DataFrame(errors,columns=['source_line','record_id','error_code']).to_csv(a.out/'rejected_rows.csv',index=False)
  note='정상 데이터에서 열 위치 의존, Scaling 누락, train() 상태는 결과를 바꿀 수 있습니다. 잘못된 수치는 별도 거부 처리해야 합니다. 기준 예측 불일치나 Config 불일치 시 이전 정상 predictions.csv를 보존합니다.'
  (a.out/'incident_notes.md').write_text('# C-02 예측 오류 원인 및 복구\n\n'+note+'\n\nSHIFT_ALERT는 오류 증명이 아닌 운영 점검 신호입니다.\n')
  write_json(a.out/'incident_report.json',manifest)
  return 0
 except (OSError,ValueError,RuntimeError,KeyError) as e:
  write_json(a.out/'incident_report.json',{**manifest,'error':str(e)})
  (a.out/'incident_notes.md').write_text('# C-02 복구 중단\n\n'+str(e)+'\n\n이전 정상 predictions.csv를 유지했습니다.\n')
  return 1
if __name__=='__main__':sys.exit(main(sys.argv[1:]))
