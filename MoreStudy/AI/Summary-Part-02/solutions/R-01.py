"""R-01 — The Last Checkpoint. CPU-only reference implementation.

The run command performs validation, v1/v2 training, v2 interruption + exact
resume in another process, validation-gated promotion, independent tests,
inference-policy audit, and row-vs-batch benchmarks. It does not require a server.
"""
from __future__ import annotations
import copy,csv,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from common import args_or_default,setup,make_mlp,binary_scores,reg_scores,predict,finite_number,write_json

F=['temperature_c','vibration','energy_kwh','alarms_7d','capacity']
H=['site_id','date','temperature_c','vibration','energy_kwh','alarms_7d','failure_next_7d','energy_next_day','final_repair_cost']
I=['site_id','date','temperature_c','vibration','energy_kwh','alarms_7d']
INTERVALS={'train':['2026-03-01','2026-06-30'],'gap1':['2026-07-01','2026-07-07'],'validation':['2026-07-08','2026-07-21'],'gap2':['2026-07-22','2026-07-28'],'test':['2026-07-29','2026-08-11']}

def atomic_json(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix='.manifest-',suffix='.tmp',delete=False,encoding='utf-8') as fh:
  temp=Path(fh.name);json.dump(obj,fh,indent=2,ensure_ascii=False);fh.flush();os.fsync(fh.fileno())
 try:os.replace(temp,path)
 finally:temp.unlink(missing_ok=True)

def atomic_checkpoint(path,state):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.tmp',delete=False) as fh:temp=Path(fh.name)
 try:
  torch.save(state,temp)
  loaded=torch.load(temp,weights_only=True,map_location='cpu')
  if 'model' not in loaded:raise ValueError('checkpoint invalid')
  os.replace(temp,path)
 finally:temp.unlink(missing_ok=True)

def get_rows(path,required):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f)
  if not set(required).issubset(reader.fieldnames or []):raise ValueError(f'missing columns in {path.name}')
  return list(reader)

def ingest(a):
 sites_raw=get_rows(a.data/'sites.csv',['site_id','zone','capacity']);sites={}
 for s in sites_raw:
  sid=(s.get('site_id') or '').strip();cap=finite_number(s.get('capacity'))
  if not sid or sid in sites or not (s.get('zone') or '').strip() or cap is None or cap<1 or cap!=int(cap):raise ValueError('INVALID_SITES_FILE')
  sites[sid]={'site_id':sid,'zone':s['zone'].strip(),'capacity':int(cap)}
 errors=[]
 def clean(source,required,history):
  raw=get_rows(a.data/source,required);valid=[];seen=set()
  for line,row in enumerate(raw,2):
   sid=(row.get('site_id') or '').strip();date=(row.get('date') or '').strip()
   values={f:finite_number(row.get(f)) for f in ['temperature_c','vibration','energy_kwh','alarms_7d']}
   targets={f:finite_number(row.get(f)) for f in ['failure_next_7d','energy_next_day']} if history else {}
   try:dtok=(pd.Timestamp(date).strftime('%Y-%m-%d')==date)
   except (ValueError,TypeError):dtok=False
   if sid not in sites:err='UNKNOWN_SITE'
   elif not dtok:err='INVALID_DATE'
   elif any(x is None for x in values.values()) or values['vibration']<0 or values['energy_kwh']<0 or values['alarms_7d']<0 or not values['alarms_7d'].is_integer():err='INVALID_VALUE'
   elif history and (targets['failure_next_7d'] not in (0,1) or targets['energy_next_day'] is None or targets['energy_next_day']<0):err='INVALID_TARGET'
   elif (sid,date) in seen:err='DUPLICATE_RECORD'
   else:err=None
   if err:errors.append({'source_file':Path(source).name,'source_line':line,'error_code':err})
   else:
    seen.add((sid,date));valid.append({'site_id':sid,'date':date,**values,**targets,**sites[sid]})
  return pd.DataFrame(valid).sort_values(['date','site_id']).reset_index(drop=True)
 history=clean('history.csv',H,True)
 # Input may be named incoming.csv when packaged outside the example data folder.
 incoming=clean('R-01/incoming.csv',I,False)
 if history.empty or incoming.empty:raise ValueError('insufficient valid records')
 pd.DataFrame(errors,columns=['source_file','source_line','error_code']).to_csv(a.out/'rejected_rows.csv',index=False)
 history.to_csv(a.out/'clean_history.csv',index=False)
 holdout=sorted(sites)[4::5]
 keep=history[~history.site_id.isin(holdout)];sets={name:keep[(keep.date>=lo)&(keep.date<=hi)] for name,(lo,hi) in INTERVALS.items()}
 if any(sets[k].empty for k in ['train','validation','test']):raise ValueError('missing split')
 audit={'valid_history':len(history),'valid_incoming':len(incoming),'rejected_count':len(errors),'error_codes':dict(Counter(e['error_code'] for e in errors)),'site_count':len(sites),'date_min':str(history.date.min()),'date_max':str(history.date.max()),'periods':INTERVALS,'holdout_site_ids':holdout,'train_count':len(sets['train']),'validation_count':len(sets['validation']),'test_A_count':len(sets['test']),'test_B_count':len(history[(history.site_id.isin(holdout))&(history.date>=INTERVALS['test'][0])&(history.date<=INTERVALS['test'][1])])}
 write_json(a.out/'data_audit.json',audit)
 return history,incoming,holdout,sets

def prepare(a,history,incoming,holdout,sets):
 train=sets['train'];raw=train[F].to_numpy(dtype='float64');mean=raw.mean(axis=0);std=raw.std(axis=0,ddof=0);std=np.where(std==0,1.,std)
 stats={'feature_order':F,'mean':mean.tolist(),'scale':std.tolist(),'training_min':raw.min(axis=0).tolist(),'training_max':raw.max(axis=0).tolist()}
 def tx(df):return torch.tensor(((df[F].to_numpy(dtype='float64')-mean)/std).astype('float32'))
 testA=sets['test'];testB=history[history.site_id.isin(holdout)&(history.date>=INTERVALS['test'][0])&(history.date<=INTERVALS['test'][1])]
 X={name:tx(df) for name,df in [('train',train),('validation',sets['validation']),('test_A',testA),('test_B',testB),('incoming',incoming)]}
 Y={name:{'classification':torch.tensor(df[['failure_next_7d']].to_numpy(dtype='float32')),'regression':torch.tensor(df[['energy_next_day']].to_numpy(dtype='float32'))} for name,df in [('train',train),('validation',sets['validation']),('test_A',testA),('test_B',testB)]}
 target_mean=float(train.energy_next_day.mean());target_std=float(train.energy_next_day.std(ddof=0)) or 1.
 stats.update({'regression_target_mean':target_mean,'regression_target_scale':target_std})
 return X,Y,stats,{'train':train,'validation':sets['validation'],'test_A':testA,'test_B':testB,'incoming':incoming}

def step_data(X,Y,task,stats):
 ys=Y[task].clone()
 if task=='regression':ys=(ys-stats['regression_target_mean'])/stats['regression_target_scale']
 return X,ys

def get_metric(task,model,valx,valy,stats):
 if task=='classification':
  probs=predict(model,valx,True);scores=[(binary_scores(valy.flatten().numpy(),probs,t)['f2'],t) for t in [.3,.5,.7]]
  return max(scores,key=lambda p:(p[0],p[1]))
 preds=predict(model,valx)*stats['regression_target_scale']+stats['regression_target_mean']
 return (reg_scores(valy.flatten().numpy(),preds)['rmse'],None)

def run_epochs(task,version,stats,x,y,vx,vy,mode,ckpt_path=None,seed=42):
 setup(seed);model=make_mlp([5,16,1]);opt=(torch.optim.SGD(model.parameters(),lr=.02,momentum=.9) if version=='v1' else torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=.01))
 sched=torch.optim.lr_scheduler.StepLR(opt,step_size=8,gamma=.5) if version=='v2' else None
 generator=torch.Generator().manual_seed(42);crit=nn.BCEWithLogitsLoss() if task=='classification' else nn.MSELoss()
 best=-float('inf') if task=='classification' else float('inf');best_state=None;best_epoch=0;best_thr=None;stale=0;history=[];start=1
 if mode=='resume':
  ck=torch.load(ckpt_path,weights_only=True,map_location='cpu')
  model.load_state_dict(ck['model']);opt.load_state_dict(ck['optimizer']);sched.load_state_dict(ck['scheduler'])
  best=ck['best_metric'];best_epoch=ck['best_epoch'];best_state=ck['best_state'];best_thr=ck['best_threshold'];stale=ck['stale'];history=ck['history'];start=ck['epoch']+1
  torch.set_rng_state(ck['torch_rng']);generator.set_state(ck['shuffle_rng'])
 stop=6 if mode=='interrupt' else 24
 for ep in range(start,stop+1):
  model.train();loader=DataLoader(TensorDataset(x,y),batch_size=32,shuffle=True,num_workers=0,generator=generator)
  sm=0
  for bx,by in loader:
   opt.zero_grad(set_to_none=True);loss=crit(model(bx),by);loss.backward();opt.step();sm+=loss.item()*len(bx)
  metric,thr=get_metric(task,model,vx,vy,stats)
  lr=opt.param_groups[0]['lr'];history.append({'version':version,'task':task,'epoch':ep,'train_loss':sm/len(x),'validation_metric':metric,'learning_rate':lr})
  better=(metric>best+1e-12 or (abs(metric-best)<=1e-12 and (best_thr is None or thr>best_thr))) if task=='classification' else metric<best-1e-12
  if better:best=metric;best_epoch=ep;best_state=copy.deepcopy(model.state_dict());best_thr=thr;stale=0
  else:stale+=1
  if sched:sched.step()
  if ckpt_path:
   atomic_checkpoint(ckpt_path,{'model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':sched.state_dict() if sched else {},'epoch':ep,'best_metric':best,'best_epoch':best_epoch,'best_state':best_state,'best_threshold':best_thr,'stale':stale,'history':history,'torch_rng':torch.get_rng_state(),'shuffle_rng':generator.get_state(),'config':{'task':task,'version':version,'feature_order':F,'mean':stats['mean'],'scale':stats['scale']}})
  if ep>=8 and version=='v2' and stale>=6 and mode!='interrupt':break
 return {'final_state':copy.deepcopy(model.state_dict()),'best_state':best_state,'best_metric':best,'best_epoch':best_epoch,'threshold':best_thr,'history':history}

def prepare_resume_data(a,X,Y,stats,task):
 payload={'x':X['train'],'y':Y['train'][task],'vx':X['validation'],'vy':Y['validation'][task],'stats':stats}
 path=a.out/'checkpoints'/f'{task}-inputs.pt';torch.save(payload,path)
 return path

def task_train(a,X,Y,stats,task,version):
 x,y=step_data(X['train'],Y['train'],task,stats);vx=X['validation'];vy=Y['validation'][task]
 if version=='v1':return run_epochs(task,version,stats,x,y,vx,vy,'continuous')
 cp=a.out/'checkpoints'/f'v2-{task}.pt'
 data_path=a.out/'checkpoints'/f'v2-{task}-prepared.pt'
 data_path.parent.mkdir(parents=True,exist_ok=True)
 torch.save({'x':x,'y':y,'vx':vx,'vy':vy,'stats':stats},data_path)
 continuous=run_epochs(task,version,stats,x,y,vx,vy,'continuous')
 run_epochs(task,version,stats,x,y,vx,vy,'interrupt',cp)
 subprocess.run([sys.executable,__file__,'--out',str(a.out),'--data',str(a.data),'--mode','resume-task','--task',task],check=True)
 resumed=torch.load(a.out/'checkpoints'/f'v2-{task}-resumed.pt',weights_only=True,map_location='cpu')
 diff=max(float((continuous['final_state'][k]-resumed['final_state'][k]).abs().max()) for k in continuous['final_state'])
 return resumed,diff

def version_predict(version_dir,task,X,stats):
 model=make_mlp([5,16,1]);model.load_state_dict(torch.load(version_dir/f'{task}.pt',weights_only=True,map_location='cpu'))
 raw=predict(model,X,task=='classification')
 if task=='regression':raw=raw*stats['regression_target_scale']+stats['regression_target_mean']
 return raw

def predict_files(a,version,stats,frames,X,manifest_update=True):
 vd=a.out/'versions'/version
 income=frames['incoming'];cls=version_predict(vd,'classification',X['incoming'],stats);reg=version_predict(vd,'regression',X['incoming'],stats)
 if not len(income):raise ValueError('no valid incoming')
 raw=income[F].to_numpy(dtype='float64');out_ratio=float(np.mean(np.any((raw<stats['training_min'])|(raw>stats['training_max']),axis=1)))
 shift=len(income)>=30 and out_ratio>.2
 threshold=json.loads((vd/'selection.json').read_text())['threshold']
 result=income[['site_id','date','zone']].copy();result['failure_probability']=cls;result['energy_prediction']=reg;result['selected']=False
 result['status']='REVIEW_REQUIRED' if shift else 'BELOW_THRESHOLD'
 if not shift:
  for (zone,date),indices in result.groupby(['zone','date'],sort=False).groups.items():
   group=result.loc[indices];eligible=group[group.failure_probability>=threshold].sort_values(['failure_probability','site_id'],ascending=[False,True]);winners=eligible.head(3)
   result.loc[eligible.index,'status']='CAPACITY_LIMIT';result.loc[winners.index,'status']='SELECTED';result.loc[winners.index,'selected']=True
 result=result[['site_id','date','failure_probability','energy_prediction','selected','status']]
 result['failure_probability']=result.failure_probability.map(lambda x:f'{x:.6f}');result['energy_prediction']=result.energy_prediction.map(lambda x:f'{x:.4f}')
 result.to_csv(vd/'incoming_predictions.csv',index=False)
 write_json(a.out/'shift_report.json',{'valid_count':len(income),'out_of_range_ratio':out_ratio,'shift_alert':shift,'status':'SHIFT_ALERT' if shift else 'OK','automatic_decisions_enabled':not shift})
 if manifest_update:
  temp=a.out/'incoming_predictions.csv.tmp';result.to_csv(temp,index=False);os.replace(temp,a.out/'incoming_predictions.csv')
 return cls,reg,shift

def rollback(a):
 path=a.out/'deployment_manifest.json'
 manifest=json.loads(path.read_text()) if path.exists() else {'active_version':None,'status':'EMPTY'}
 prev=manifest.get('previous_version')
 if not prev:
  write_json(a.out/'rollback_report.json',{'status':'NO_ROLLBACK_TARGET'});return False
 saved=a.out/'versions'/prev/'incoming_predictions.csv'
 if not saved.exists():write_json(a.out/'rollback_report.json',{'status':'MISSING_PREVIOUS_VERSION'});return False
 temp=a.out/'incoming_predictions.csv.tmp';shutil.copy2(saved,temp);os.replace(temp,a.out/'incoming_predictions.csv')
 atomic_json(path,{**manifest,'active_version':prev,'previous_version':manifest.get('active_version'),'status':'ACTIVE'})
 write_json(a.out/'rollback_report.json',{'status':'ROLLED_BACK','active_version':prev});return True

def benchmark(a,version,X,stats):
 vd=a.out/'versions'/version; modelc=make_mlp([5,16,1]);modelr=make_mlp([5,16,1]);modelc.load_state_dict(torch.load(vd/'classification.pt',weights_only=True));modelr.load_state_dict(torch.load(vd/'regression.pt',weights_only=True));modelc.eval();modelr.eval();x=X['incoming']
 def run_row():
  c=[];r=[]
  with torch.inference_mode():
   for xi in x:
    c.append(float(torch.sigmoid(modelc(xi.unsqueeze(0))).item()))
    r.append(float(modelr(xi.unsqueeze(0)).item()))
  return np.asarray(c),np.asarray(r)
 def run_batch():
  with torch.inference_mode():return torch.sigmoid(modelc(x)).flatten().numpy(),modelr(x).flatten().numpy()
 times={};pred={}
 for label,fn in [('row',run_row),('batch',run_batch)]:
  fn();arr=[]
  for _ in range(5):
   st=time.perf_counter();p=fn();arr.append(time.perf_counter()-st)
  times[label]=float(np.median(arr));pred[label]=p
 diff=max(float(np.max(np.abs(pred['row'][i]-pred['batch'][i]))) for i in [0,1])
 result={'row_median_seconds':times['row'],'batch_median_seconds':times['batch'],'max_abs_diff':diff,'results_match':diff<=1e-6,'samples':len(x)}
 write_json(a.out/'benchmark.json',result)
 if diff>1e-6:raise ValueError('benchmark predictions mismatch')
 return result

def incoming_only(a):
    """Production inference: validate only sites and incoming, never history Targets."""
    sites={}
    for r in get_rows(a.data/'sites.csv',['site_id','zone','capacity']):
        sid=(r.get('site_id') or '').strip();cap=finite_number(r.get('capacity'))
        if not sid or sid in sites or not (r.get('zone') or '').strip() or cap is None or cap<1 or cap!=int(cap):
            raise ValueError('INVALID_SITES_FILE')
        sites[sid]={'capacity':int(cap),'zone':r['zone'].strip()}
    rows=get_rows(a.data/'R-01'/'incoming.csv',I);valid=[];errors=[];seen=set()
    for line,r in enumerate(rows,2):
        site=(r.get('site_id') or '').strip();date=(r.get('date') or '').strip()
        numbers={k:finite_number(r.get(k)) for k in ['temperature_c','vibration','energy_kwh','alarms_7d']}
        try:valid_date=(pd.Timestamp(date).strftime('%Y-%m-%d')==date)
        except (TypeError,ValueError):valid_date=False
        if site not in sites:err='UNKNOWN_SITE'
        elif not valid_date:err='INVALID_DATE'
        elif any(v is None for v in numbers.values()) or numbers['vibration']<0 or numbers['energy_kwh']<0 or numbers['alarms_7d']<0 or not numbers['alarms_7d'].is_integer():err='INVALID_VALUE'
        elif (site,date) in seen:err='DUPLICATE_RECORD'
        else:err=None
        if err:errors.append({'source_file':'incoming.csv','source_line':line,'error_code':err})
        else:
            seen.add((site,date));valid.append({'site_id':site,'date':date,**numbers,**sites[site]})
    if not valid:raise ValueError('no valid incoming records')
    pd.DataFrame(errors,columns=['source_file','source_line','error_code']).to_csv(a.out/'rejected_rows.csv',index=False)
    return pd.DataFrame(valid).sort_values(['date','site_id']).reset_index(drop=True)

def main(argv=None):
 import argparse
 # Keep compatible CLI while accepting the internal --task for subprocess resumption.
 av=list(sys.argv[1:] if argv is None else argv)
 task=None
 if '--task' in av:
  idx=av.index('--task');task=av[idx+1];del av[idx:idx+2]
 a=args_or_default(av,'R-01')
 if a.mode=='rollback':rollback(a);return
 if a.mode=='resume-task':
  if task not in ['classification','regression']:raise ValueError('task')
  payload=torch.load(a.out/'checkpoints'/f'v2-{task}-prepared.pt',weights_only=True,map_location='cpu')
  state=run_epochs(task,'v2',payload['stats'],payload['x'],payload['y'],payload['vx'],payload['vy'],'resume',a.out/'checkpoints'/f'v2-{task}.pt')
  torch.save(state,a.out/'checkpoints'/f'v2-{task}-resumed.pt');return
 if a.mode not in ('run','validate','train','predict','evaluate','promote','benchmark'):raise ValueError('unknown mode')
 if a.mode in ('predict','benchmark'):
  manifest=json.loads((a.out/'deployment_manifest.json').read_text());version=manifest['active_version']
  if not version:raise ValueError('no active deployment')
  saved=json.loads((a.out/'versions'/version/'preprocessing.json').read_text())
  if saved['feature_order']!=F:raise ValueError('incompatible feature order')
  income=incoming_only(a)
  tensor=torch.tensor(((income[F].to_numpy(dtype='float64')-saved['mean'])/saved['scale']).astype('float32'))
  if a.mode=='predict':predict_files(a,version,saved,{'incoming':income},{'incoming':tensor})
  else:benchmark(a,version,{'incoming':tensor},saved)
  return
 history,incoming,holdout,sets=ingest(a)
 if a.mode=='validate':return
 X,Y,stats,frames=prepare(a,history,incoming,holdout,sets)
 results={};histrows=[];resume_diff={}
 for version in ['v1','v2']:
  results[version]={};vd=a.out/'versions'/version;vd.mkdir(parents=True,exist_ok=True)
  for task in ['classification','regression']:
   if version=='v2':r,diff=task_train(a,X,Y,stats,task,version);resume_diff[task]=diff
   else:r=task_train(a,X,Y,stats,task,version)
   results[version][task]=r;histrows+=r['history']
   torch.save(r['best_state'],vd/f'{task}.pt')
  write_json(vd/'preprocessing.json',stats)
  write_json(vd/'selection.json',{'threshold':results[version]['classification']['threshold'],'classification_best_epoch':results[version]['classification']['best_epoch'],'regression_best_epoch':results[version]['regression']['best_epoch']})
 pd.DataFrame(histrows).to_csv(a.out/'training_history.csv',index=False)
 matched=all(diff<=1e-6 for diff in resume_diff.values())
 write_json(a.out/'resume_audit.json',{'interrupted_after_epoch':6,'resumed_from_epoch':7,'max_parameter_diff_by_task':resume_diff,'max_parameter_diff':max(resume_diff.values()),'matched':matched})
 if not matched:raise ValueError('exact resume failed')
 v1=results['v1'];v2=results['v2']
 f2a=v1['classification']['best_metric'];f2b=v2['classification']['best_metric'];rmsea=v1['regression']['best_metric'];rmseb=v2['regression']['best_metric']
 promote=(f2b>=f2a-1e-12 and rmseb<=rmsea+1e-12 and (f2b>f2a+1e-12 or rmseb<rmsea-1e-12));selected='v2' if promote else 'v1'
 write_json(a.out/'validation_selection.json',{'v1':{'classification_f2':f2a,'regression_rmse':rmsea},'v2':{'classification_f2':f2b,'regression_rmse':rmseb},'selected_version':selected,'reason':'VALIDATION_PROMOTION_RULE' if promote else 'V1_RETAINED'})
 if a.mode=='train':return
 evaluations={}
 for subset in ['test_A','test_B']:
  c=version_predict(a.out/'versions'/selected,'classification',X[subset],stats)
  r=version_predict(a.out/'versions'/selected,'regression',X[subset],stats)
  evaluations[subset]={'classification':binary_scores(frames[subset].failure_next_7d,c,results[selected]['classification']['threshold']),'regression':reg_scores(frames[subset].energy_next_day,r),'baseline_classification':binary_scores(frames[subset].failure_next_7d,np.full(len(c),int(frames['train'].failure_next_7d.mean()>=.5))),'baseline_regression':reg_scores(frames[subset].energy_next_day,frames[subset].energy_kwh)}
 write_json(a.out/'test_evaluation.json',evaluations)
 if a.mode=='evaluate':return
 # Retain the previously deployed v1 result for a real rollback target.
 predict_files(a,'v1',stats,frames,X,manifest_update=False)
 # Retain v1 as first valid deployed version before considering v2 promotion.
 old={'active_version':'v1','previous_version':None,'status':'ACTIVE','model_paths':{t:f'versions/v1/{t}.pt' for t in ['classification','regression']}}
 path=a.out/'deployment_manifest.json'
 if not path.exists() or json.loads(path.read_text()).get('active_version') is None:atomic_json(path,old)
 cls,reg,shift=predict_files(a,selected,stats,frames,X,manifest_update=False)
 bench=benchmark(a,selected,X,stats)
 if selected=='v2':
  manifest={'active_version':'v2','previous_version':'v1','status':'ACTIVE','model_paths':{t:f'versions/v2/{t}.pt' for t in ['classification','regression']},'validation_checked':True,'resume_checked':matched}
 else:manifest={**old,'validation_checked':True,'resume_checked':matched}
 if not bench['results_match']:raise ValueError('benchmark mismatch')
 # Publish only after the model, reference checks and benchmark have passed.
 staged=a.out/'incoming_predictions.csv.tmp'
 shutil.copy2(a.out/'versions'/selected/'incoming_predictions.csv',staged)
 os.replace(staged,a.out/'incoming_predictions.csv')
 atomic_json(path,manifest)
 (a.out/'final_report.md').write_text('# R-01 — The Last Checkpoint\n\n- 분할: 시설 Holdout + 7일 Gap을 포함한 고정 날짜 분할\n- 사후 수리비 및 Target을 Feature에서 제외\n- Classification: 검증 F2, Threshold 동점은 높은 값 우선\n- Regression: 검증 RMSE로 Best Weight 선정\n- Resume: 별도 Python 프로세스에서 Epoch 7부터 재개; 모델·Optimizer·Scheduler·난수·Shuffle·Best State 복원\n- v2 승격 여부는 Validation 결과로만 선택; Test는 독립 평가\n- 버전별 모델 파일 보존 후 Manifest 원자적 갱신\n- 분포 변화 경보가 자동 점검 정책과 분리됨\n- 행별 추론과 Batch 추론의 결과 일치 검사\n\n'+f'- 최종 버전: {selected}\n- 최대 Resume Parameter 차이: {max(resume_diff.values()):.9g}\n- Benchmark 결과 최대 차이: {bench["max_abs_diff"]:.9g}\n')
if __name__=='__main__':main(sys.argv[1:])
