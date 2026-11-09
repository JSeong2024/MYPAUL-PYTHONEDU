"""A-04: separate train/predict commands. Only trusted weights_only checkpoints."""
import copy,csv,json,sys
import numpy as np
import pandas as pd
import torch
from torch import nn
from common import args_or_default,setup,scale,make_mlp,train_epoch,predict,binary_scores,finite_number,write_json
F=['temperature_c','vibration','hours_active']

def train(a):
 setup();df=pd.read_csv(a.data/'training.csv');parts=[df[df.split==s].copy() for s in ('train','validation','test')];tr,va,te=parts
 x,[vx,ex],mean,std=scale(tr[F].to_numpy(),[va[F].to_numpy(),te[F].to_numpy()])
 xx=torch.tensor(x);yy=torch.tensor(tr[['needs_service']].to_numpy(dtype='float32'));vxx=torch.tensor(vx);vyy=torch.tensor(va[['needs_service']].to_numpy(dtype='float32'))
 model=make_mlp([3,8,1]);opt=torch.optim.AdamW(model.parameters(),lr=.01);criterion=nn.BCEWithLogitsLoss()
 best=float('inf');be=0;bs=None
 for epoch in range(1,51):
  train_epoch(model,opt,criterion,xx,yy,16,epoch)
  model.eval()
  with torch.inference_mode():l=float(criterion(model(vxx),vyy))
  if l<best-1e-12:best=l;be=epoch;bs=copy.deepcopy(model.state_dict())
 model.load_state_dict(bs)
 pre_probs=predict(model,torch.tensor(ex),True)
 torch.save(model.state_dict(),a.out/'model_weights.pt')
 write_json(a.out/'preprocessing.json',{'feature_order':F,'mean':mean.tolist(),'scale':std.tolist(),'target':'needs_service','threshold':.5,'best_epoch':be,'model_architecture':[3,8,1],'dtype':'float32'})
 loaded=make_mlp([3,8,1]);loaded.load_state_dict(torch.load(a.out/'model_weights.pt',map_location='cpu',weights_only=True))
 probs=predict(loaded,torch.tensor(ex),True);actual=te.needs_service.to_numpy()
 pd.DataFrame({'record_id':te.record_id,'actual':actual,'probability':[f'{p:.6f}' for p in probs],'predicted':(probs>=.5).astype(int)}).to_csv(a.out/'test_predictions.csv',index=False)
 write_json(a.out/'handoff_report.json',{'feature_order':F,'test_accuracy':binary_scores(actual,probs)['accuracy'],'reload_max_abs_diff':float(np.max(np.abs(pre_probs-probs)))})

def run_predict(a):
 meta=json.loads((a.out/'preprocessing.json').read_text());cols=meta['feature_order']
 if cols!=F or meta.get('model_architecture')!=[3,8,1]:raise ValueError('incompatible config')
 with (a.data/'incoming.csv').open(newline='',encoding='utf-8-sig') as f:
  rd=csv.DictReader(f)
  if not set(['record_id']+cols).issubset(rd.fieldnames or []):raise ValueError('missing required feature')
  rows=list(rd)
 model=make_mlp([3,8,1]);model.load_state_dict(torch.load(a.out/'model_weights.pt',map_location='cpu',weights_only=True))
 accepted=[];rejected=[];seen=set()
 for row in rows:
  rid=(row.get('record_id') or '').strip();vals=[finite_number(row.get(f)) for f in cols]
  if not rid or any(v is None for v in vals):error='INVALID_VALUE'
  elif rid in seen:error='DUPLICATE_ID'
  else:error=None
  if error:rejected.append({'record_id':rid,'error_code':error})
  else:seen.add(rid);accepted.append((rid,vals))
 probs=[]
 if accepted:
  raw=np.asarray([row[1] for row in accepted]);scaled=((raw-meta['mean'])/meta['scale']).astype('float32')
  probs=predict(model,torch.tensor(scaled),True)
 pd.DataFrame([{'record_id':rid,'probability':f'{p:.6f}','predicted':int(p>=meta['threshold'])} for (rid,_),p in zip(accepted,probs)],columns=['record_id','probability','predicted']).to_csv(a.out/'incoming_predictions.csv',index=False)
 pd.DataFrame(rejected,columns=['record_id','error_code']).to_csv(a.out/'rejected_rows.csv',index=False)

def main(argv=None):
 a=args_or_default(argv,'A-04')
 if a.mode=='predict':run_predict(a)
 elif a.mode in ('run','train'):
  train(a)
  if a.mode=='run':run_predict(a)
 else:raise ValueError('mode must be run/train/predict')
if __name__=='__main__':main(sys.argv[1:])
