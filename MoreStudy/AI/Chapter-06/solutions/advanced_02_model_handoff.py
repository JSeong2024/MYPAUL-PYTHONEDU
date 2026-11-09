"""Advanced 02 — 학습된 신경망 상태와 전처리 정보를 함께 보관/복원."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

ROOT=Path(__file__).resolve().parents[1]
FEATURES=[f'f{i}' for i in range(1,7)]

class TriageNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers=nn.Sequential(nn.Linear(6,24),nn.ReLU(),nn.Dropout(0.15),nn.Linear(24,3))
    def forward(self,x):
        if x.ndim != 2 or x.shape[1] != 6:
            raise ValueError('Feature Shape는 (batch, 6)이어야 합니다.')
        return self.layers(x)


def validate_features(frame):
    if list(frame.columns)!=FEATURES:
        raise ValueError(f'Feature 열과 순서는 {FEATURES}이어야 합니다.')
    arr=frame.to_numpy(dtype=np.float32)
    if not np.isfinite(arr).all():
        raise ValueError('결측값 또는 무한대가 포함되어 있습니다.')
    return arr


def predict(model,frame,mean,std):
    features=validate_features(frame)
    values=(features-mean)/std
    model.eval()
    with torch.inference_mode():
        logits=model(torch.tensor(values,dtype=torch.float32))
        probs=logits.softmax(dim=1).numpy()
    return probs


def run(data_path=ROOT/'data/triage_signals.csv',output_dir=None):
    torch.set_num_threads(1)
    torch.manual_seed(41)
    df=pd.read_csv(data_path)
    x=validate_features(df[FEATURES])
    labels=df['class_id'].to_numpy(dtype=int)
    if not np.isin(labels,[0,1,2]).all():
        raise ValueError('class_id는 0, 1, 2여야 합니다.')
    ids=np.arange(len(df))
    trainval,test=train_test_split(ids,test_size=0.20,random_state=51,stratify=labels)
    train,val=train_test_split(trainval,test_size=0.25,random_state=52,stratify=labels[trainval])
    # Train에서만 전처리 통계량을 계산합니다.
    mean=x[train].mean(axis=0)
    std=x[train].std(axis=0)
    std=np.where(std==0,1.0,std)
    scaled=(x-mean)/std
    feats=torch.tensor(scaled,dtype=torch.float32)
    y=torch.tensor(labels,dtype=torch.int64)
    model=TriageNet()
    optim=torch.optim.Adam(model.parameters(),lr=0.018)
    best_loss=float('inf');best_state=None
    # 학습 중 Validation Loss가 가장 낮은 상태를 선택. Test는 마지막에 한 번 사용.
    for epoch in range(180):
        model.train();optim.zero_grad()
        loss=nn.CrossEntropyLoss()(model(feats[train]),y[train])
        loss.backward();optim.step()
        model.eval()
        with torch.inference_mode():
            val_loss=float(nn.CrossEntropyLoss()(model(feats[val]),y[val]))
        if val_loss < best_loss:
            best_loss=val_loss
            best_state={k:v.detach().clone() for k,v in model.state_dict().items()}
    model.load_state_dict(best_state)
    probs=predict(model,df.iloc[test][FEATURES],mean,std)
    predictions=probs.argmax(axis=1)
    report={'test_accuracy':float(accuracy_score(labels[test],predictions)),
            'test_macro_f1':float(f1_score(labels[test],predictions,average='macro')),
            'train_count':len(train),'validation_count':len(val),'test_count':len(test)}
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        torch.save(model.state_dict(),out/'model_weights.pt')
        metadata={'features':FEATURES,'mean':mean.tolist(),'std':std.tolist(),'num_classes':3,'architecture':'TriageNet'}
        (out/'model_metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding='utf-8')
        (out/'evaluation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        pd.DataFrame({'event_id':df.iloc[test]['event_id'].to_numpy(),'true_label':labels[test],
                      'predicted_label':predictions,'confidence':probs.max(axis=1)}).to_csv(out/'predictions.csv',index=False)
        restored=TriageNet()
        restored.load_state_dict(torch.load(out/'model_weights.pt',map_location='cpu',weights_only=True))
        metadata_saved=json.loads((out/'model_metadata.json').read_text(encoding='utf-8'))
        restored_probs=predict(restored,df.iloc[test][metadata_saved['features']],np.asarray(metadata_saved['mean']),np.asarray(metadata_saved['std']))
        if not np.allclose(probs,restored_probs,atol=1e-6):
            raise RuntimeError('복원된 모델의 예측이 일치하지 않습니다.')
    print('Test accuracy:',round(report['test_accuracy'],3),'Macro F1:',round(report['test_macro_f1'],3))
    return report,model,(mean,std),test

if __name__=='__main__':
    run(output_dir=ROOT/'outputs/advanced_02')
