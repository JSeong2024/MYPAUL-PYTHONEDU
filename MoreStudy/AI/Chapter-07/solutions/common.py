"""Chapter 07 모범 구현에서 공유하는 데이터 처리·학습 함수."""
from __future__ import annotations
from pathlib import Path
import random
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

ROOT=Path(__file__).resolve().parents[1]
ENERGY_FEATURES=['hour','temperature_c','occupancy','is_weekend']
ALERT_FEATURES=['vibration','temperature_c','load_factor','days_since_service']

def seed_everything(seed: int=42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)

def read_frame(path: Path, features: list[str], target: str, id_col: str) -> pd.DataFrame:
    df=pd.read_csv(path)
    cols=[id_col,*features,target]
    if any(c not in df.columns for c in cols):
        raise ValueError(f'Required columns: {cols}')
    if df[id_col].isna().any() or df[id_col].duplicated().any():
        raise ValueError('ID must be unique and nonmissing')
    if df.empty or not np.isfinite(df[features+[target]].to_numpy(dtype=float)).all():
        raise ValueError('Numeric values must be finite and data nonempty')
    return df

def energy_data(path: Path | None=None):
    """시간 순서에 따른 240/60/60 분할. 모든 Scaling은 Train에서 계산."""
    df=read_frame(Path(path) if path else ROOT/'data/energy_demand.csv',
                  ENERGY_FEATURES,'demand_kwh','observation_id')
    if len(df)<120: raise ValueError('Need at least 120 rows')
    n=len(df);a=int(n*2/3);b=int(n*5/6)
    raw=df[ENERGY_FEATURES].to_numpy(dtype=np.float32)
    tar=df['demand_kwh'].to_numpy(dtype=np.float32).reshape(-1,1)
    mean=raw[:a].mean(0);std=raw[:a].std(0);std=np.where(std<1e-8,1.,std)
    ymean=float(tar[:a].mean());ystd=float(tar[:a].std());ystd=max(ystd,1e-8)
    x=torch.from_numpy(((raw-mean)/std).astype('float32'))
    y=torch.from_numpy(((tar-ymean)/ystd).astype('float32'))
    return {'train':(x[:a],y[:a]),'validation':(x[a:b],y[a:b]),
            'test':(x[b:],y[b:]),'mean':mean,'std':std,'ymean':ymean,
            'ystd':ystd,'df':df,'test_indices':list(range(b,n))}

def alert_data(path: Path | None=None):
    df=read_frame(Path(path) if path else ROOT/'data/device_alerts.csv',
                  ALERT_FEATURES,'alert_label','event_id')
    if not set(df.alert_label.unique()).issubset({0,1}):raise ValueError('Labels must be binary')
    ix=np.arange(len(df));label=df.alert_label.to_numpy(dtype=int)
    tr,remaining=train_test_split(ix,test_size=.4,random_state=42,stratify=label)
    va,te=train_test_split(remaining,test_size=.5,random_state=42,stratify=label[remaining])
    raw=df[ALERT_FEATURES].to_numpy(dtype=np.float32)
    mean=raw[tr].mean(0);std=raw[tr].std(0);std=np.where(std<1e-8,1.,std)
    x=torch.from_numpy(((raw-mean)/std).astype(np.float32))
    y=torch.from_numpy(label.astype(np.float32).reshape(-1,1))
    return {'train':(x[tr],y[tr]),'validation':(x[va],y[va]),'test':(x[te],y[te]),
            'mean':mean,'std':std,'df':df,'indices':{'train':tr,'validation':va,'test':te}}

def make_loader(x:torch.Tensor,y:torch.Tensor, batch_size:int=32,shuffle:bool=False,seed:int=42):
    gen=torch.Generator().manual_seed(seed)
    return DataLoader(TensorDataset(x,y),batch_size=batch_size,shuffle=shuffle,generator=gen)

def regression_model(hidden:int=24,dropout:float=0.) -> nn.Module:
    return nn.Sequential(nn.Linear(4,hidden),nn.ReLU(),nn.Dropout(dropout),nn.Linear(hidden,1))

def binary_model(hidden:int=16) -> nn.Module:
    return nn.Sequential(nn.Linear(4,hidden),nn.ReLU(),nn.Linear(hidden,1))

def train_epoch(model:nn.Module,loader:DataLoader,optimizer:torch.optim.Optimizer,
                loss_fn:nn.Module,clip_norm:float|None=None) -> float:
    model.train();total=0.;samples=0
    for x,y in loader:
        optimizer.zero_grad(set_to_none=True)
        loss=loss_fn(model(x),y)
        if not bool(torch.isfinite(loss).item()):raise FloatingPointError('Non-finite loss')
        loss.backward()
        if clip_norm is not None:nn.utils.clip_grad_norm_(model.parameters(),clip_norm)
        optimizer.step()
        batch=len(x);total+=float(loss.detach())*batch;samples+=batch
    return total/samples

def eval_loss(model:nn.Module,x:torch.Tensor,y:torch.Tensor,loss_fn:nn.Module) -> float:
    model.eval()
    with torch.inference_mode():return float(loss_fn(model(x),y).item())

def eval_regression(model:nn.Module,x:torch.Tensor,y:torch.Tensor,ymean:float,ystd:float):
    model.eval()
    with torch.inference_mode():
        pred=(model(x).numpy()*ystd+ymean).flatten()
        truth=(y.numpy()*ystd+ymean).flatten()
    return {'mae':float(np.mean(np.abs(pred-truth))),
            'rmse':float(np.sqrt(np.mean((pred-truth)**2))),
            'pred':pred,'truth':truth}

def no_nan(model:nn.Module)->bool:
    return all(torch.isfinite(p).all().item() for p in model.parameters())
