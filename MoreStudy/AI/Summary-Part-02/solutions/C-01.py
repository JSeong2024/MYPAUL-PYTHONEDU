"""C-01: exact resume across fresh Python processes with atomic checkpointing."""
import copy,json,os,shutil,sys,tempfile,subprocess
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader
from common import args_or_default,setup,make_mlp,write_json
EPOCHS=20

def atomic_checkpoint(path,state):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.checkpoint-',suffix='.tmp',delete=False) as f:
  tmp=Path(f.name)
 try:
  torch.save(state,tmp)
  # Check integrity before touching the currently valid checkpoint.
  verified=torch.load(tmp,weights_only=True,map_location='cpu')
  if 'model_state' not in verified:raise ValueError('checkpoint verification')
  if path.exists():shutil.copy2(path,path.with_suffix('.bak'))
  os.replace(tmp,path)
 finally:tmp.unlink(missing_ok=True)

def read_data(a):
 tr=pd.read_csv(a.data/'train.csv');va=pd.read_csv(a.data/'validation.csv');features=['f1','f2','f3','f4']
 return (torch.tensor(tr[features].to_numpy(dtype='float32')),torch.tensor(tr[['label']].to_numpy(dtype='float32')),torch.tensor(va[features].to_numpy(dtype='float32')),torch.tensor(va[['label']].to_numpy(dtype='float32')))

def run(a,mode):
 setup();x,y,vx,vy=read_data(a)
 model=make_mlp([4,16,1],dropout=.2)
 opt=torch.optim.AdamW(model.parameters(),lr=.005);scheduler=torch.optim.lr_scheduler.StepLR(opt,step_size=5,gamma=.5)
 generator=torch.Generator().manual_seed(42)
 criterion=nn.BCEWithLogitsLoss();history=[];best=float('inf');best_epoch=0;best_state=None
 start=1;target=EPOCHS if mode in ('continuous','resume') else 8
 if mode=='resume':
  ck=torch.load(a.out/'checkpoint.pt',map_location='cpu',weights_only=True)
  expected={'model_state','optimizer_state','scheduler_state','completed_epoch','cpu_rng_state','shuffle_generator_state','history','best_metric','best_epoch','best_model_state'}
  if not expected.issubset(ck):raise ValueError('checkpoint missing fields')
  model.load_state_dict(ck['model_state']);opt.load_state_dict(ck['optimizer_state']);scheduler.load_state_dict(ck['scheduler_state'])
  history=ck['history'];best=ck['best_metric'];best_epoch=ck['best_epoch'];best_state=ck['best_model_state']
  # Restore RNG only after models and optimizers have been instantiated.
  torch.set_rng_state(ck['cpu_rng_state']);generator.set_state(ck['shuffle_generator_state'])
  start=ck['completed_epoch']+1
 for epoch in range(start,target+1):
  model.train();loader=DataLoader(TensorDataset(x,y),batch_size=16,shuffle=True,num_workers=0,generator=generator)
  total=0
  for bx,by in loader:
   opt.zero_grad(set_to_none=True);loss=criterion(model(bx),by);loss.backward();opt.step();total+=loss.item()*len(bx)
  model.eval()
  with torch.inference_mode():vl=float(criterion(model(vx),vy))
  lr=opt.param_groups[0]['lr']
  history.append({'epoch':epoch,'train_loss':total/len(x),'validation_loss':vl,'learning_rate':lr})
  if vl<best-1e-12:best=vl;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
  scheduler.step()
  if mode in ('interrupt','resume'):
   state={'model_state':model.state_dict(),'optimizer_state':opt.state_dict(),'scheduler_state':scheduler.state_dict(),'completed_epoch':epoch,'cpu_rng_state':torch.get_rng_state(),'shuffle_generator_state':generator.get_state(),'history':history,'best_metric':best,'best_epoch':best_epoch,'best_model_state':best_state}
   atomic_checkpoint(a.out/'checkpoint.pt',state)
 stem='continuous' if mode=='continuous' else 'resumed'
 pd.DataFrame(history).to_csv(a.out/f'{stem}_history.csv',index=False)
 torch.save(model.state_dict(),a.out/f'{stem}_final_weights.pt')
 if mode=='interrupt':(a.out/'interrupt_log.json').write_text(json.dumps({'completed_epoch':8}))
 return history

def comparison(a):
 h1=pd.read_csv(a.out/'continuous_history.csv');h2=pd.read_csv(a.out/'resumed_history.csv')
 if len(h1)!=20 or len(h2)!=20:raise AssertionError('history size')
 w1=torch.load(a.out/'continuous_final_weights.pt',weights_only=True);w2=torch.load(a.out/'resumed_final_weights.pt',weights_only=True)
 pdiff=max(float((w1[k]-w2[k]).abs().max()) for k in w1)
 lrdiff=float(np.max(np.abs(h1.learning_rate.to_numpy()-h2.learning_rate.to_numpy())))
 lossdiff=float(np.max(np.abs(h1[['train_loss','validation_loss']].to_numpy()-h2[['train_loss','validation_loss']].to_numpy())))
 matched=pdiff<=1e-6 and lrdiff<=1e-12 and lossdiff<=1e-6
 write_json(a.out/'resume_audit.json',{'completed_epoch':20,'resumed_from_epoch':9,'max_parameter_diff':pdiff,'max_lr_diff':lrdiff,'max_loss_diff':lossdiff,'matched':matched})
 (a.out/'recovery_report.md').write_text('# C-01 학습 중단 복구\n\n모델 Weight만 저장하면 AdamW의 누적 상태, Scheduler 단계, Dropout 난수 및 Shuffle 순서를 복구할 수 없습니다.\n\n- 중단 지점: Epoch 8 종료 직후\n- 저장: Model·Optimizer·Scheduler·CPU RNG·Loader Generator·Best Weight·이력\n- 복원: 모델·Optimizer 구성 이후 RNG State 적용\n- Checkpoint 임시 파일 검증 및 원자적 교체, 이전 버전 백업\n- 결과: '+('일치' if matched else '불일치 — 추가 점검 필요')+f'\n- 최대 Parameter 차이: {pdiff:.10g}\n- 최대 Epoch Loss 차이: {lossdiff:.10g}\n')
 if not matched:raise AssertionError('resume differs from continuous')

def main(argv=None):
 a=args_or_default(argv,'C-01');mode=a.mode
 if mode=='run':
  run(a,'continuous')
  subprocess.run([sys.executable,__file__,'--data',str(a.data),'--out',str(a.out),'--mode','interrupt'],check=True)
  subprocess.run([sys.executable,__file__,'--data',str(a.data),'--out',str(a.out),'--mode','resume'],check=True)
  comparison(a)
 elif mode in ('continuous','interrupt','resume'):run(a,mode)
 elif mode=='compare':comparison(a)
 else:raise ValueError('unrecognized mode')
if __name__=='__main__':main(sys.argv[1:])
