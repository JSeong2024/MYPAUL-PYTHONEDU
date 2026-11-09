"""Mini 01 — XOR 신호: 단일 Linear와 MLP 비교."""
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]


def fit(model, x, y, epochs=230, lr=0.025):
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        logits = model(x).squeeze(1)
        loss = loss_fn(logits, y)
        loss.backward()
        optimizer.step()
        history.append(float(loss.item()))
    return history


def accuracy(model, x, y):
    model.eval()
    with torch.inference_mode():
        probs = torch.sigmoid(model(x).squeeze(1))
        preds = (probs >= 0.5).long()
    return float((preds == y.long()).float().mean().item()), probs.cpu().numpy()


def run(data_path=ROOT/'data/xor_signals.csv', output_dir=None):
    torch.set_num_threads(1)
    torch.manual_seed(11)
    df=pd.read_csv(data_path)
    required={'sample_id','signal_x','signal_y','label'}
    if not required.issubset(df) or df[['signal_x','signal_y','label']].isna().any().any():
        raise ValueError('필수 열 또는 값이 누락되었습니다.')
    if not np.isfinite(df[['signal_x','signal_y']].to_numpy(dtype=float)).all() or not df['label'].isin([0,1]).all():
        raise ValueError('유효하지 않은 Feature 또는 Label입니다.')
    idx_train, idx_test = train_test_split(np.arange(len(df)),test_size=0.25,stratify=df['label'],random_state=17)
    x = torch.tensor(df[['signal_x','signal_y']].to_numpy(dtype='float32'))
    y = torch.tensor(df['label'].to_numpy(dtype='float32'))
    x_train,y_train=x[idx_train],y[idx_train]
    x_test,y_test=x[idx_test],y[idx_test]
    linear=nn.Linear(2,1)
    mlp=nn.Sequential(nn.Linear(2,8),nn.Tanh(),nn.Linear(8,1))
    history_linear=fit(linear,x_train,y_train)
    history_mlp=fit(mlp,x_train,y_train)
    acc_linear,probs_linear=accuracy(linear,x_test,y_test)
    acc_mlp,probs_mlp=accuracy(mlp,x_test,y_test)
    report=pd.DataFrame({'model':['linear','mlp'],'test_accuracy':[acc_linear,acc_mlp],
                         'parameter_count':[sum(p.numel() for p in m.parameters()) for m in (linear,mlp)]})
    predictions=pd.DataFrame({'sample_id':df.iloc[idx_test]['sample_id'].to_numpy(),
                              'true_label':y_test.long().numpy(),
                              'linear_probability':probs_linear,'mlp_probability':probs_mlp})
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        report.to_csv(out/'model_comparison.csv',index=False)
        predictions.to_csv(out/'predictions.csv',index=False)
    print(f'Linear accuracy: {acc_linear:.3f}, MLP accuracy: {acc_mlp:.3f}')
    return report, predictions, history_linear,history_mlp

if __name__=='__main__':
    run(output_dir=ROOT/'outputs/mini_01')
