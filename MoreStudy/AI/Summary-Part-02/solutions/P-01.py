"""P-01: group-independent fleet risk training and capacity-limited review."""
import csv,copy,sys
from datetime import datetime
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import GroupShuffleSplit
from common import args_or_default,setup,scale,make_mlp,train_epoch,predict,binary_scores,finite_number,write_json
F=['temperature_c','vibration_mm_s','alarm_count_7d','operating_hours']

def validate(path,source,incoming=False):
 required=['record_id','site_id','asset_id','recorded_date']+F+([] if incoming else ['failure_next_7d','final_repair_cost'])
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f)
  if not set(required).issubset(reader.fieldnames or []):raise ValueError(f'{source}: missing columns')
  rows=list(reader)
 valid=[];errors=[];seen=set()
 for line,row in enumerate(rows,2):
  rid=(row.get('record_id') or '').strip();ids=[(row.get(k) or '').strip() for k in ['site_id','asset_id']]
  nums=[finite_number(row.get(k)) for k in F]
  try:dt=datetime.strptime(row['recorded_date'],'%Y-%m-%d').date();date_ok=dt.isoformat()==row['recorded_date']
  except (TypeError,ValueError):date_ok=False
  if not rid or any(not v for v in ids) or not date_ok or any(v is None for v in nums):error='INVALID_VALUE'
  elif any(v<0 for v in nums[1:]) or nums[2]!=int(nums[2]):error='INVALID_VALUE'
  elif not incoming and finite_number(row.get('final_repair_cost')) is None:error='INVALID_VALUE'
  elif not incoming and (finite_number(row.get('failure_next_7d')) not in (0,1)):error='INVALID_TARGET'
  elif rid in seen:error='DUPLICATE_ID'
  else:error=None
  if error:errors.append({'source_file':source,'source_line':line,'record_id':rid,'error_code':error})
  else:
   seen.add(rid);valid.append({**row,**dict(zip(F,nums)),'record_id':rid,**dict(zip(['site_id','asset_id'],ids)),**({} if incoming else {'failure_next_7d':int(float(row['failure_next_7d']))})})
 return pd.DataFrame(valid,columns=required),errors

def priority_policy(incoming,probs,threshold):
 frame=incoming[['record_id','site_id','asset_id','recorded_date']].copy();frame['probability']=probs;frame['selected']=False;frame['status']='BELOW_THRESHOLD'
 for (site,date),ids in frame.groupby(['site_id','recorded_date'],sort=False).groups.items():
  pool=frame.loc[ids];passing=pool[pool.probability>=threshold]
  if passing.empty:continue
  winners=passing.sort_values(['probability','record_id'],ascending=[False,True]).drop_duplicates('asset_id')
  selected=winners.sort_values(['probability','asset_id','record_id'],ascending=[False,True,True]).head(5)
  winner_ids=set(winners.index);selected_ids=set(selected.index)
  for idx in passing.index:
   frame.at[idx,'status']='SELECTED' if idx in selected_ids else 'CAPACITY_LIMIT' if idx in winner_ids else 'DUPLICATE_ASSET'
   frame.at[idx,'selected']=idx in selected_ids
 frame['probability']=frame['probability'].map(lambda x:f'{x:.6f}')
 return frame

def main(argv=None):
 a=args_or_default(argv,'P-01');setup()
 hist,e1=validate(a.data/'maintenance_history.csv','maintenance_history.csv')
 incoming,e2=validate(a.data/'incoming_maintenance.csv','incoming_maintenance.csv',True)
 pd.DataFrame(e1+e2,columns=['source_file','source_line','record_id','error_code']).to_csv(a.out/'invalid_records.csv',index=False)
 groups=hist.site_id.to_numpy();gss=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42)
 tv_i,te_i=next(gss.split(hist,groups=groups));tv=hist.iloc[tv_i];test=hist.iloc[te_i]
 gss=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42)
 tr_i,va_i=next(gss.split(tv,groups=tv.site_id));train=tv.iloc[tr_i];val=tv.iloc[va_i]
 site_sets=[set(t.site_id) for t in [train,val,test]]
 audit={k:{'samples':len(df),'sites':len(set(df.site_id))} for k,df in zip(['train','validation','test'],[train,val,test])}
 audit.update({'intersection_train_validation':len(site_sets[0]&site_sets[1]),'intersection_train_test':len(site_sets[0]&site_sets[2]),'intersection_validation_test':len(site_sets[1]&site_sets[2])})
 write_json(a.out/'split_audit.json',audit)
 counts=train.failure_next_7d.value_counts();neg=int(counts.get(0,0));pos=int(counts.get(1,0))
 if not neg or not pos:raise ValueError('train split missing a class')
 x,[vx,ex,ix],mean,std=scale(train[F].to_numpy(),[val[F].to_numpy(),test[F].to_numpy(),incoming[F].to_numpy()])
 xx=torch.tensor(x);yy=torch.tensor(train[['failure_next_7d']].to_numpy(dtype='float32'));valx=torch.tensor(vx);valy=torch.tensor(val[['failure_next_7d']].to_numpy(dtype='float32'))
 model=make_mlp([4,16,8,1]);opt=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.01)
 posweight=neg/pos;criterion=nn.BCEWithLogitsLoss(pos_weight=torch.tensor(posweight,dtype=torch.float32))
 best=float('inf');be=0;bs=None;stale=0;histrows=[]
 for epoch in range(1,81):
  loss=train_epoch(model,opt,criterion,xx,yy,32,epoch)
  model.eval()
  with torch.inference_mode():vloss=float(criterion(model(valx),valy))
  histrows.append({'epoch':epoch,'train_loss':loss,'validation_loss':vloss})
  if vloss<best-1e-12:best=vloss;be=epoch;bs=copy.deepcopy(model.state_dict());stale=0
  else:stale+=1
  if stale>=8:break
 model.load_state_dict(bs)
 valprob=predict(model,valx,True);thresh=max([.25,.4,.55,.7],key=lambda t:(binary_scores(val.failure_next_7d,valprob,t)['f2'],t))
 testprob=predict(model,torch.tensor(ex),True);base=int(pos>neg)
 model_scores=binary_scores(test.failure_next_7d,testprob,thresh)
 base_scores=binary_scores(test.failure_next_7d,np.full(len(test),base),.5)
 pd.DataFrame(histrows).to_csv(a.out/'training_history.csv',index=False)
 write_json(a.out/'evaluation.json',{'best_epoch':be,'pos_weight':posweight,'threshold':thresh,'baseline':base_scores,'model':model_scores})
 priority_policy(incoming,predict(model,torch.tensor(ix),True),thresh).to_csv(a.out/'incoming_priorities.csv',index=False)
 torch.save(model.state_dict(),a.out/'model_weights.pt')
 write_json(a.out/'preprocessing.json',{'feature_order':F,'mean':mean.tolist(),'scale':std.tolist(),'threshold':thresh,'best_epoch':be,'model_architecture':[4,16,8,1]})
 loaded=make_mlp([4,16,8,1]);loaded.load_state_dict(torch.load(a.out/'model_weights.pt',weights_only=True,map_location='cpu'))
 assert np.max(np.abs(predict(loaded,torch.tensor(ex),True)-testprob))<=1e-6
if __name__=='__main__':main(sys.argv[1:])
