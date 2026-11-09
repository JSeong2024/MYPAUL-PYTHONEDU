"""Advanced 01 — 신경망 Shape, Parameter, 출력 형태 검사."""
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

ROOT=Path(__file__).resolve().parents[1]
FEATURES=[f'f{i}' for i in range(1,7)]

class SignalNet(nn.Module):
    def __init__(self,hidden=16,dropout=0.0):
        super().__init__()
        self.layers=nn.Sequential(nn.Linear(6,hidden),nn.ReLU(),nn.Dropout(dropout),nn.Linear(hidden,3))
    def forward(self,x):
        if x.ndim!=2 or x.shape[1]!=6:
            raise ValueError('입력 Shape는 (batch, 6)이어야 합니다.')
        return self.layers(x)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def train(model,x,y,epochs=160):
    optim=torch.optim.Adam(model.parameters(),lr=0.018)
    for _ in range(epochs):
        model.train();optim.zero_grad()
        loss=nn.CrossEntropyLoss()(model(x),y)
        loss.backward();optim.step()


def run(data_path=ROOT/'data/triage_signals.csv',output_dir=None):
    torch.set_num_threads(1)
    torch.manual_seed(31)
    df=pd.read_csv(data_path)
    if not set(FEATURES+['class_id']).issubset(df) or not np.isfinite(df[FEATURES].to_numpy(dtype=float)).all() or not df['class_id'].isin([0,1,2]).all():
        raise ValueError('입력 데이터가 올바르지 않습니다.')
    train_idx,val_idx=train_test_split(np.arange(len(df)),test_size=0.3,stratify=df.class_id,random_state=13)
    x=torch.tensor(df[FEATURES].to_numpy(dtype='float32'))
    y=torch.tensor(df.class_id.to_numpy(dtype='int64'))
    model_small=SignalNet(8,0.0)
    model_large=SignalNet(32,0.1)
    rows=[]
    for name,model in [('small',model_small),('large',model_large)]:
        train(model,x[train_idx],y[train_idx])
        model.eval()
        with torch.inference_mode():
            logits=model(x[val_idx])
            predictions=logits.argmax(dim=1).numpy()
        rows.append({'architecture':name,'parameter_count':count_parameters(model),'validation_macro_f1':f1_score(y[val_idx],predictions,average='macro')})
    report=pd.DataFrame(rows)
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        report.to_csv(out/'architecture_comparison.csv',index=False)
    print(report.to_string(index=False))
    return report,model_small,model_large

if __name__=='__main__':
    run(output_dir=ROOT/'outputs/advanced_01')
