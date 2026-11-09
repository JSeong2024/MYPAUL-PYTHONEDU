"""Professional 01 — 신규 Site의 정비 위험 분류 및 검토 용량 정책.

실제 설비 정비 의사결정이 아닌 실습용 합성 데이터 분석입니다.
"""
from __future__ import annotations
from pathlib import Path
import copy
import json
import math
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import fbeta_score,precision_score,recall_score
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.common import seed_everything,make_loader,train_epoch,eval_loss

FEATURES=['equipment_type','vibration','temperature_c','utilization',
          'days_since_service','prior_alerts']
LEAKAGE_COLUMNS={'post_inspection_result','maintenance_label'}
SITES={'train':['S01','S02','S03','S04'],'validation':['S05'],'test':['S06']}

def validate_source(path):
    df=pd.read_csv(path)
    required=['event_id','site_id','device_id','week',*FEATURES,
              'post_inspection_result','maintenance_label']
    if not set(required).issubset(df.columns):
        raise ValueError(f'Missing columns: {sorted(set(required)-set(df.columns))}')
    if df.empty or df.event_id.isna().any() or df.event_id.duplicated().any():
        raise ValueError('event_id must be unique and nonmissing')
    if df[['site_id','device_id']].isna().any().any():
        raise ValueError('Site and device identifiers cannot be missing')
    values=df[[*FEATURES,'week','maintenance_label']].to_numpy(dtype=float)
    if not np.isfinite(values).all():raise ValueError('Non-finite feature/label')
    if not set(df.maintenance_label.unique()).issubset({0,1}):
        raise ValueError('maintenance_label must be binary')
    if not set(df.site_id.unique()).issubset(set(sum(SITES.values(),[]))):
        raise ValueError('Unknown site')
    if df.duplicated(subset=['device_id','week']).any():
        raise ValueError('Duplicate device-week')
    return df

def network(name):
    if name=='linear':return nn.Linear(len(FEATURES),1)
    if name=='mlp':return nn.Sequential(nn.Linear(len(FEATURES),18),nn.ReLU(),nn.Linear(18,1))
    raise ValueError(f'Unknown network: {name}')

def predict_probability(model,x):
    model.eval()
    with torch.inference_mode():
        return torch.sigmoid(model(x)).numpy().reshape(-1)

def capacity_check(weeks,flags,max_review_fraction):
    """각 주차의 검토 건수가 ceil(frac * 주차 건수) 이하여야 함."""
    summary=pd.DataFrame({'week':np.asarray(weeks),'review_flag':np.asarray(flags,dtype=int)})
    counts=summary.groupby('week').review_flag.agg(['size','sum'])
    limits=np.ceil(counts['size'].to_numpy()*max_review_fraction).astype(int)
    over=(counts['sum'].to_numpy()>limits)
    return bool(not over.any()),int(over.sum())

def select_threshold(y,prob,weeks,max_review_fraction=.30):
    if len(y)!=len(prob) or len(y)!=len(weeks):raise ValueError('Length mismatch')
    candidates=[]
    for threshold in np.linspace(.10,.95,18):
        pred=(prob>=threshold).astype(int)
        is_ok,_=capacity_check(weeks,pred,max_review_fraction)
        if is_ok:
            candidates.append({'threshold':float(threshold),
                               'validation_f2':float(fbeta_score(y,pred,beta=2,zero_division=0)),
                               'validation_review_rate':float(pred.mean())})
    if not candidates:raise ValueError('No feasible validation threshold')
    # 성능이 같다면 검토 건수가 적은 정책, 그래도 같다면 높은 Threshold 선택.
    return max(candidates,key=lambda r:(r['validation_f2'],
                                        -r['validation_review_rate'],r['threshold']))

def run(data_path=None,output_dir=None,max_epochs=24,patience=6,
        max_review_fraction=.30):
    if max_epochs<2 or patience<1 or not 0<max_review_fraction<=1:
        raise ValueError('Invalid training parameters')
    seed_everything(1729)
    path=Path(data_path) if data_path else Path(__file__).resolve().parents[1]/'data/fleet_events.csv'
    df=validate_source(path)
    splits={name:df.loc[df.site_id.isin(sites)].copy()
            for name,sites in SITES.items()}
    if any(len(frame)==0 for frame in splits.values()):
        raise ValueError('Each site split needs data')
    train=splits['train'];validation=splits['validation'];test=splits['test']
    raw_train=train[FEATURES].to_numpy(dtype=np.float32)
    mean=raw_train.mean(0);std=raw_train.std(0)
    std=np.where(std<1e-8,1.,std)
    def as_tensors(frame):
        raw=frame[FEATURES].to_numpy(dtype=np.float32)
        x=torch.from_numpy(((raw-mean)/std).astype(np.float32))
        y=torch.from_numpy(frame.maintenance_label.to_numpy(dtype=np.float32).reshape(-1,1))
        return x,y
    xtr,ytr=as_tensors(train);xva,yva=as_tensors(validation);xte,yte=as_tensors(test)
    positives=float(ytr.sum());negatives=len(ytr)-positives
    if not positives or not negatives:raise ValueError('Train requires both classes')
    pos_weight=torch.tensor([negatives/positives],dtype=torch.float32)
    loss_fn=nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    history=[];candidate_reports=[];candidate_models={}
    for name in ['linear','mlp']:
        seed_everything(2030)
        model=network(name)
        optimizer=torch.optim.AdamW(model.parameters(),lr=.012 if name=='linear' else .009,
                                    weight_decay=.025)
        loader=make_loader(xtr,ytr,batch_size=32,shuffle=True,seed=71)
        best_val=float('inf');best_state=None;best_epoch=0;stale=0
        for epoch in range(1,max_epochs+1):
            train_loss=train_epoch(model,loader,optimizer,loss_fn,clip_norm=2.)
            val_loss=eval_loss(model,xva,yva,loss_fn)
            history.append({'model':name,'epoch':epoch,'train_loss':train_loss,
                            'validation_loss':val_loss})
            if val_loss<best_val-1e-7:
                best_val=val_loss;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch;stale=0
            else:
                stale+=1
                if stale>=patience:break
        model.load_state_dict(best_state)
        prob=predict_probability(model,xva)
        candidate=select_threshold(yva.numpy().flatten().astype(int),prob,
                                   validation.week.to_numpy(),max_review_fraction)
        candidate_reports.append({'model':name,'best_epoch':best_epoch,
            'best_validation_loss':best_val,**candidate})
        candidate_models[name]=model
    # 모델·Threshold는 Validation 데이터만으로 확정.
    winner=max(candidate_reports,key=lambda r:(r['validation_f2'],
                     -r['validation_review_rate'],-r['best_validation_loss']))
    selected=winner['model'];threshold=winner['threshold'];model=candidate_models[selected]
    # 이 시점부터 Test 평가: 모델 선택·Threshold 수정에 사용하지 않음.
    prob=predict_probability(model,xte)
    pred=(prob>=threshold).astype(int)
    true=yte.numpy().flatten().astype(int)
    capacity_ok,over_weeks=capacity_check(test.week,pred,max_review_fraction)
    recalls={}
    for equipment_type,sub in test.groupby('equipment_type'):
        idx=test.index.get_indexer(sub.index)
        recalls[str(int(equipment_type))]=float(recall_score(true[idx],pred[idx],zero_division=0))
    report={
        'selected_model':selected,'selected_threshold':threshold,
        'best_epoch':int(winner['best_epoch']),
        'validation_f2':float(winner['validation_f2']),
        'validation_review_rate':float(winner['validation_review_rate']),
        'max_review_fraction':max_review_fraction,
        'test_f2':float(fbeta_score(true,pred,beta=2,zero_division=0)),
        'test_precision':float(precision_score(true,pred,zero_division=0)),
        'test_recall':float(recall_score(true,pred,zero_division=0)),
        'test_review_rate':float(pred.mean()),
        'test_capacity_ok':capacity_ok,
        'test_over_capacity_weeks':over_weeks,
        'test_recall_by_equipment_type':recalls,
        'split_sizes':{name:len(frame) for name,frame in splits.items()},
        'site_ids':SITES,
        'post_inspection_used_as_feature':False,
    }
    prediction_frame=pd.DataFrame({
        'event_id':test.event_id.to_numpy(),'site_id':test.site_id.to_numpy(),
        'week':test.week.to_numpy(),'true_label':true,
        'risk_probability':prob.round(6),'review_flag':pred,
    })
    meta={'model':selected,'features':FEATURES,'train_mean':mean.tolist(),
          'train_std':std.tolist(),'threshold':threshold,
          'max_review_fraction':max_review_fraction,'model_version':'chapter07-v1'}
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        pd.DataFrame(candidate_reports).to_csv(out/'candidate_scores.csv',index=False)
        pd.DataFrame(history).to_csv(out/'training_history.csv',index=False)
        prediction_frame.to_csv(out/'test_predictions.csv',index=False)
        (out/'evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        (out/'metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
        torch.save(model.state_dict(),out/'model_weights.pt')
        restored=network(selected)
        restored.load_state_dict(torch.load(out/'model_weights.pt',weights_only=True,map_location='cpu'))
        error=float(np.max(np.abs(predict_probability(restored,xte)-prob)))
        if error>1e-6:raise AssertionError('Restore mismatch')
    return report,pd.DataFrame(candidate_reports),prediction_frame

if __name__=='__main__':
    result,_,_=run(output_dir=Path(__file__).resolve().parents[1]/'outputs'/'professional_01')
    print(json.dumps(result,indent=2))
