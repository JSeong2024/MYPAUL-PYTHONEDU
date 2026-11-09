"""Mini 02 — 비선형 수요 예측: Linear vs MLP."""
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import train_test_split

ROOT=Path(__file__).resolve().parents[1]


def train(model,x,y,epochs=320,lr=0.025):
    optimizer=torch.optim.Adam(model.parameters(),lr=lr)
    loss_fn=nn.MSELoss()
    history=[]
    for _ in range(epochs):
        optimizer.zero_grad()
        loss=loss_fn(model(x).squeeze(1),y)
        loss.backward()
        optimizer.step()
        history.append(loss.item())
    return history


def run(data_path=ROOT/'data/nonlinear_demand.csv', output_dir=None):
    torch.set_num_threads(1)
    torch.manual_seed(21)
    df=pd.read_csv(data_path)
    needed=['temperature_scaled','load_scaled','demand']
    if not set(needed).issubset(df) or not np.isfinite(df[needed].to_numpy(dtype=float)).all():
        raise ValueError('필수 데이터에 결측값 또는 무한대가 있습니다.')
    train_idx,test_idx=train_test_split(np.arange(len(df)),test_size=0.25,random_state=23)
    x=torch.tensor(df[needed[:2]].to_numpy(dtype='float32'))
    y=torch.tensor(df['demand'].to_numpy(dtype='float32'))
    # 스케일링이 필요한 경우 반드시 Train만으로 학습합니다. 여기서는 이미 [-1.6,1.6] 범위의 Feature 사용.
    linear=nn.Linear(2,1)
    mlp=nn.Sequential(nn.Linear(2,24),nn.Tanh(),nn.Linear(24,12),nn.Tanh(),nn.Linear(12,1))
    hl=train(linear,x[train_idx],y[train_idx])
    hm=train(mlp,x[train_idx],y[train_idx])
    linear.eval()
    mlp.eval()
    with torch.inference_mode():
        pl=linear(x[test_idx]).squeeze(1).numpy()
        pm=mlp(x[test_idx]).squeeze(1).numpy()
    actual=y[test_idx].numpy()
    rmse_l=float(np.sqrt(np.mean((actual-pl)**2)))
    rmse_m=float(np.sqrt(np.mean((actual-pm)**2)))
    report=pd.DataFrame({'model':['linear','mlp'],'test_rmse':[rmse_l,rmse_m]})
    predictions=pd.DataFrame({'record_id':df.iloc[test_idx]['record_id'].to_numpy(),'actual':actual,'linear_prediction':pl,'mlp_prediction':pm})
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        report.to_csv(out/'regression_comparison.csv',index=False)
        predictions.to_csv(out/'predictions.csv',index=False)
    print(f'Linear RMSE: {rmse_l:.3f}, MLP RMSE: {rmse_m:.3f}')
    return report,predictions,hl,hm

if __name__=='__main__':
    run(output_dir=ROOT/'outputs/mini_02')
