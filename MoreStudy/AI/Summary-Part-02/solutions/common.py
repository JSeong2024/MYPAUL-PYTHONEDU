"""Common PyTorch utilities; CPU-only and deterministic by default."""
from __future__ import annotations
import copy, json, math, os, tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score,fbeta_score,confusion_matrix,mean_absolute_error,mean_squared_error

torch.set_num_threads(1)

def setup(seed=42):
    torch.manual_seed(seed);np.random.seed(seed)

def make_mlp(sizes,dropout=0):
    mods=[]
    for i in range(len(sizes)-1):
        mods.append(nn.Linear(sizes[i],sizes[i+1]))
        if i<len(sizes)-2:
            mods.append(nn.ReLU())
            if dropout:mods.append(nn.Dropout(dropout))
    return nn.Sequential(*mods)

def scale(train,other):
    avg=train.mean(axis=0);std=train.std(axis=0,ddof=0);std=np.where(std==0,1.,std)
    return ((train-avg)/std).astype('float32'), [((o-avg)/std).astype('float32') for o in other],avg,std

def vectors(df,features,target=None):
    x=torch.tensor(df[features].to_numpy(dtype='float32'))
    if target is None:return x
    return x,torch.tensor(df[target].to_numpy(dtype='float32').reshape(-1,1))

def binary_scores(actual,probs,threshold=.5):
    pred=(np.asarray(probs)>=threshold).astype(int);y=np.asarray(actual).astype(int)
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {'accuracy':float(accuracy_score(y,pred)),'f1':float(f1_score(y,pred,zero_division=0)),'recall':float(recall_score(y,pred,zero_division=0)),'precision':float(precision_score(y,pred,zero_division=0)),'f2':float(fbeta_score(y,pred,beta=2,zero_division=0)), 'tp':int(tp),'fp':int(fp),'fn':int(fn),'tn':int(tn)}

def reg_scores(y,p):
    y=np.asarray(y,dtype=float);p=np.asarray(p,dtype=float)
    return {'mae':float(np.mean(np.abs(y-p))),'rmse':float(np.sqrt(np.mean((y-p)**2)))}

def predict(model,x,binary=False,batch_size=256):
    model.eval();out=[]
    with torch.inference_mode():
        for b in x.split(batch_size):
            p=model(b).flatten()
            out.extend((p.sigmoid() if binary else p).numpy().tolist())
    return np.asarray(out)

def train_epoch(model,optim,criterion,x,y,batch_size,epoch,seed=42):
    model.train();generator=torch.Generator().manual_seed(seed+epoch)
    loader=DataLoader(TensorDataset(x,y),batch_size=batch_size,shuffle=True,generator=generator,num_workers=0)
    loss_sum=0.;samples=0
    for bx,by in loader:
        optim.zero_grad(set_to_none=True)
        loss=criterion(model(bx),by)
        loss.backward();optim.step()
        loss_sum+=loss.item()*len(bx);samples+=len(bx)
    return loss_sum/samples

def train_best(model,optim,criterion,x,y,vx,vy,epochs=50,batch_size=16,metric='loss',early=None,scheduler=None,seed=42):
    best_metric=float('-inf') if metric in ('accuracy','f2') else float('inf')
    best_state=None;best_epoch=0;rows=[];stale=0
    for epoch in range(1,epochs+1):
        tl=train_epoch(model,optim,criterion,x,y,batch_size,epoch,seed)
        pred=predict(model,vx,binary=metric in ('accuracy','f2','loss_binary'))
        if metric=='accuracy':m=binary_scores(vy.flatten().numpy(),pred)['accuracy']
        elif metric=='f2':m=binary_scores(vy.flatten().numpy(),pred)['f2']
        elif metric=='rmse':m=reg_scores(vy.flatten().numpy(),pred)['rmse']
        else:
            model.eval()
            with torch.inference_mode():m=float(criterion(model(vx),vy))
        rows.append({'epoch':epoch,'train_loss':tl,'validation_metric':m})
        improved=m>best_metric+1e-12 if metric in ('accuracy','f2') else m<best_metric-1e-12
        if improved:
            best_metric=m;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch;stale=0
        else:stale+=1
        if scheduler is not None:
            if isinstance(scheduler,torch.optim.lr_scheduler.ReduceLROnPlateau):scheduler.step(m)
            else:scheduler.step()
        if early is not None and stale>=early:break
    model.load_state_dict(best_state)
    return rows,{'best_epoch':best_epoch,'best_metric':best_metric}

def write_json(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda o:float(o)))

def load(path):return pd.read_csv(path)

def args_or_default(argv,default):
    from argparse import ArgumentParser
    ap=ArgumentParser();ap.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1]/'data');ap.add_argument('--out',type=Path,default=Path('outputs')/default);ap.add_argument('--mode',default='run');args=ap.parse_args(argv);args.out.mkdir(parents=True,exist_ok=True);return args

def finite_number(s):
    try:
        x=float(s)
        return x if np.isfinite(x) else None
    except (TypeError,ValueError):return None
