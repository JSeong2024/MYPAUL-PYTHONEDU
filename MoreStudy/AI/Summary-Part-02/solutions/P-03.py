"""P-03: 3 runs per architecture/batch strategy, equal update budgets."""
import copy,sys,time
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader
from common import args_or_default,setup,scale,make_mlp,predict,binary_scores,write_json
F=['f1','f2','f3','f4'];STRUCT={'S':[4,8,1],'L':[4,32,16,1]}

def gradients(model,criterion,xb,yb,strategy):
 model.zero_grad(set_to_none=True)
 parts=[(xb,yb)] if strategy=='A' else [(xb[i:i+32],yb[i:i+32]) for i in range(0,len(xb),32)]
 for xx,yy in parts:
  loss=criterion(model(xx),yy)*(len(xx)/len(xb));loss.backward()
 return [p.grad.detach().clone() for p in model.parameters()]

def run(sizes,strategy,x,y,initial,run_id,max_updates=120):
 model=make_mlp(sizes);model.load_state_dict(copy.deepcopy(initial));opt=torch.optim.AdamW(model.parameters(),lr=.005);criterion=nn.BCEWithLogitsLoss()
 updates=0;elapsed=0.;epoch=0;rows=len(x)
 while updates<max_updates:
  epoch+=1;generator=torch.Generator().manual_seed(1000+epoch)
  perm=torch.randperm(rows,generator=generator)
  for start in range(0,rows,64):
   if updates>=max_updates:break
   ids=perm[start:start+64];bx=x[ids];by=y[ids]
   tic=time.perf_counter();gradients(model,criterion,bx,by,strategy)
   nn.utils.clip_grad_norm_(model.parameters(),max_norm=1.0);opt.step();elapsed+=time.perf_counter()-tic
   updates+=1
 return model,elapsed,updates

def main(argv=None):
 a=args_or_default(argv,'P-03');setup();df=pd.read_csv(a.data/'quality_train.csv')
 tr,va,te=[df[df.split==v].copy() for v in ['train','validation','test']]
 tx,[vx,ex],_,_=scale(tr[F].to_numpy(),[va[F].to_numpy(),te[F].to_numpy()]);x=torch.tensor(tx);y=torch.tensor(tr[['defective']].to_numpy(dtype='float32'));valx=torch.tensor(vx);testx=torch.tensor(ex)
 runs=[];comps=[];snapshots={};initials={}
 for name,sizes in STRUCT.items():
  setup();initial=copy.deepcopy(make_mlp(sizes).state_dict());initials[name]=initial
  for strategy in ['A','B']:
   vals=[];times=[]
   for run_id in [1,2,3]:
    model,elapsed,updates=run(sizes,strategy,x,y,initial,run_id)
    p=predict(model,valx,True);scores=binary_scores(va.defective,p)
    criterion=nn.BCEWithLogitsLoss();model.eval()
    with torch.inference_mode():vl=float(criterion(model(valx),torch.tensor(va[['defective']].to_numpy(dtype='float32'))))
    runs.append({'architecture':name,'batch_strategy':strategy,'run_id':run_id,'optimizer_updates':updates,'validation_loss':vl,'validation_accuracy':scores['accuracy'],'elapsed_seconds':elapsed})
    vals.append(scores['accuracy']);times.append(elapsed)
    if run_id==1:snapshots[(name,strategy)]=copy.deepcopy(model.state_dict())
   comps.append({'architecture':name,'batch_strategy':strategy,'parameter_count':sum(p.numel() for p in make_mlp(sizes).parameters()),'median_seconds':float(np.median(times)),'mean_validation_accuracy':float(np.mean(vals))})
 chosen=sorted(comps,key=lambda r:(-r['mean_validation_accuracy'],r['median_seconds'],r['architecture']!='S',r['batch_strategy']!='A'))[0]
 name=chosen['architecture'];strategy=chosen['batch_strategy']
 model=make_mlp(STRUCT[name]);model.load_state_dict(snapshots[(name,strategy)])
 score=binary_scores(te.defective,predict(model,testx,True))
 audit={}
 for arch,sizes in STRUCT.items():
  model=make_mlp(sizes);model.load_state_dict(initials[arch]);xb=x[:min(64,len(x))];yb=y[:len(xb)]
  ga=gradients(model,nn.BCEWithLogitsLoss(),xb,yb,'A');gb=gradients(model,nn.BCEWithLogitsLoss(),xb,yb,'B')
  audit[arch]=float(max((p-q).abs().max() for p,q in zip(ga,gb)))
 pd.DataFrame(runs).to_csv(a.out/'runs.csv',index=False)
 pd.DataFrame(comps).to_csv(a.out/'comparison.csv',index=False)
 write_json(a.out/'selected_model.json',{'architecture':name,'batch_strategy':strategy,'best_validation_accuracy':chosen['mean_validation_accuracy'],'test_accuracy':score['accuracy'],'test_f1':score['f1']})
 write_json(a.out/'gradient_audit.json',{'max_abs_diff_by_architecture':audit,'max_abs_diff':max(audit.values())})
 (a.out/'training_report.md').write_text('# P-03 학습 실험 기록\n\n- 각 구성에서 정확히 120회 Optimizer Update 실행\n- Batch A: 최대 64개, Batch B: 최대 32개 Micro-Batch 누적\n- 최종 불완전 Batch를 포함해 실제 샘플 수로 Loss 가중\n- 각 설정 3회, 학습 Update 구간만 측정\n- 후보 선택: Validation 평균 Accuracy, 시간 중앙값, 구조 S, 전략 A 순\n- CPU 환경과 연산 순서에 따라 수치·시간 차이가 발생할 수 있음\n')
if __name__=='__main__':main(sys.argv[1:])
