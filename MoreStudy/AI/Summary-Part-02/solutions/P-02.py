"""P-02: temporal (day-level) split with 1-day gap and residual audit."""
import copy,csv,sys
import numpy as np
import pandas as pd
import torch
from torch import nn
from common import args_or_default,setup,scale,make_mlp,train_epoch,predict,reg_scores,finite_number,write_json
F=['energy_kwh','temperature_c','weekday','holiday','alarm_count']

def validate(path):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f)
  required=['grid_id','date']+F+['next_day_energy_kwh']
  if not set(required).issubset(reader.fieldnames or []):raise ValueError('missing columns')
  raw=list(reader)
 valid=[];invalid=[];seen=set()
 for line,r in enumerate(raw,2):
  key=(r.get('grid_id'),r.get('date'))
  try:
   parsed=pd.Timestamp(r['date']);dt_ok=parsed.strftime('%Y-%m-%d')==r['date']
  except (TypeError,ValueError):dt_ok=False
  vals={f:finite_number(r.get(f)) for f in F+['next_day_energy_kwh']}
  if not r.get('grid_id') or not dt_ok:error='INVALID_DATE'
  elif any(v is None for v in vals.values()) or any(vals[f]<0 for f in ['energy_kwh','alarm_count','next_day_energy_kwh']) or vals['weekday'] not in range(7) or vals['holiday'] not in (0,1) or vals['alarm_count']!=int(vals['alarm_count']):error='INVALID_VALUE'
  elif key in seen:error='DUPLICATE_RECORD'
  else:error=None
  if error:invalid.append({'source_line':line,'grid_id':key[0],'date':key[1],'error_code':error})
  else:seen.add(key);valid.append({**r,**vals})
 return pd.DataFrame(valid),pd.DataFrame(invalid,columns=['source_line','grid_id','date','error_code'])

def main(argv=None):
 a=args_or_default(argv,'P-02');setup();df,reject=validate(a.data/'microgrid_daily.csv')
 reject.to_csv(a.out/'invalid_daily.csv',index=False)
 dates=sorted(df.date.unique());D=len(dates)
 if D<40:raise ValueError('insufficient dates')
 ntrain=int(np.floor(.6*D));nval=int(np.floor(.2*D))
 # Remove the last day of each preceding period as specified in the problem.
 train_dates=dates[:ntrain-1]; gap1=dates[ntrain-1];val_dates=dates[ntrain:ntrain+nval-1];gap2=dates[ntrain+nval-1];test_dates=dates[ntrain+nval:]
 write_json(a.out/'split_dates.json',{'train':{'count':len(train_dates),'first':train_dates[0],'last':train_dates[-1]},'validation':{'count':len(val_dates),'first':val_dates[0],'last':val_dates[-1]},'test':{'count':len(test_dates),'first':test_dates[0],'last':test_dates[-1]},'gap_dates':[gap1,gap2]})
 tr=df[df.date.isin(train_dates)];v=df[df.date.isin(val_dates)];te=df[df.date.isin(test_dates)]
 xx,[vx,ex],mean,std=scale(tr[F].to_numpy(),[v[F].to_numpy(),te[F].to_numpy()]);x=torch.tensor(xx);y=torch.tensor(tr[['next_day_energy_kwh']].to_numpy(dtype='float32'))
 model=make_mlp([5,24,1]);opt=torch.optim.AdamW(model.parameters(),lr=.003)
 sched=torch.optim.lr_scheduler.ReduceLROnPlateau(opt,mode='min',factor=.5,patience=5);criterion=nn.MSELoss()
 best=float('inf');be=0;bs=None;stale=0;hist=[]
 for epoch in range(1,121):
  lr=opt.param_groups[0]['lr'];tl=train_epoch(model,opt,criterion,x,y,32,epoch)
  rmse=reg_scores(v.next_day_energy_kwh,predict(model,torch.tensor(vx)))['rmse']
  hist.append({'epoch':epoch,'train_mse':tl,'validation_rmse':rmse,'learning_rate':lr})
  if rmse<best-1e-12:best=rmse;be=epoch;bs=copy.deepcopy(model.state_dict());stale=0
  else:stale+=1
  sched.step(rmse)
  if stale>=15:break
 model.load_state_dict(bs)
 pred=predict(model,torch.tensor(ex));actual=te.next_day_energy_kwh.to_numpy();base=te.energy_kwh.to_numpy();resid=actual-pred
 pd.DataFrame(hist).to_csv(a.out/'training_history.csv',index=False)
 write_json(a.out/'model_comparison.json',{'baseline':reg_scores(actual,base),'mlp':reg_scores(actual,pred),'best_epoch':be})
 out=te[['grid_id','date']].copy();out['actual']=actual;out['baseline_prediction']=base;out['model_prediction']=pred;out['residual']=resid
 for f in ['actual','baseline_prediction','model_prediction','residual']:out[f]=out[f].map(lambda t:f'{t:.4f}')
 out.to_csv(a.out/'test_predictions.csv',index=False)
 groups=pd.DataFrame({'grid_id':te.grid_id,'abs_error':np.abs(resid)}).groupby('grid_id',sort=True).agg(sample_count=('abs_error','size'),mae=('abs_error','mean')).reset_index()
 groups.to_csv(a.out/'grid_report.csv',index=False,float_format='%.4f')
 top=te[['grid_id','date']].copy();top['actual']=actual;top['model_prediction']=pred;top['residual']=resid
 top=top.sort_values(['residual','date','grid_id'],ascending=[False,True,True]).head(5)
 top.to_csv(a.out/'underprediction_top5.csv',index=False,float_format='%.4f')
 torch.save(model.state_dict(),a.out/'model_weights.pt')
 write_json(a.out/'preprocessing.json',{'feature_order':F,'mean':mean.tolist(),'scale':std.tolist(),'split_dates':{'train':train_dates,'validation':val_dates,'test':test_dates,'gap':[gap1,gap2]},'architecture':[5,24,1],'best_epoch':be,'optimizer':'AdamW','learning_rate':.003})
 loaded=make_mlp([5,24,1]);loaded.load_state_dict(torch.load(a.out/'model_weights.pt',weights_only=True,map_location='cpu'))
 assert np.max(np.abs(pred-predict(loaded,torch.tensor(ex))))<1e-6
if __name__=='__main__':main(sys.argv[1:])
