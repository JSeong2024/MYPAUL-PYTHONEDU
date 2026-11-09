"""Advanced 02 — Micro-Batch 가중 평균과 Gradient Clipping 검증."""
from __future__ import annotations
from pathlib import Path
import copy
import numpy as np
import pandas as pd
import torch
from torch import nn
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.common import alert_data,seed_everything


def flat_gradient(model: nn.Module) -> torch.Tensor:
    return torch.cat([p.grad.detach().flatten() for p in model.parameters()])


def run(data_path=None,output_dir=None,clip_max_norm:float=.3):
    if clip_max_norm<=0:raise ValueError('clip_max_norm must be positive')
    seed_everything(42)
    d=alert_data(data_path)
    x,y=d['train'];x,y=x[:11],y[:11]
    template=nn.Linear(4,1);state=copy.deepcopy(template.state_dict())
    loss_fn=nn.BCEWithLogitsLoss(reduction='mean')
    full=nn.Linear(4,1);full.load_state_dict(state);full.zero_grad(set_to_none=True)
    loss_fn(full(x),y).backward()
    gradient_full=flat_gradient(full).clone()

    micro=nn.Linear(4,1);micro.load_state_dict(state);micro.zero_grad(set_to_none=True)
    for start in range(0,len(x),4):
        xm,ym=x[start:start+4],y[start:start+4]
        loss=loss_fn(micro(xm),ym)
        (loss * (len(xm)/len(x))).backward()  # 마지막 불완전 Batch 크기도 반영
    gradient_micro=flat_gradient(micro).clone()
    before=float(torch.linalg.vector_norm(gradient_micro))
    # clipping은 전체 Micro-Batch가 누적된 뒤 한 번만 실행합니다.
    nn.utils.clip_grad_norm_(micro.parameters(),max_norm=clip_max_norm)
    clipped=flat_gradient(micro).clone()
    after=float(torch.linalg.vector_norm(clipped))
    abs_difference=float((gradient_full-gradient_micro).abs().max())
    audit={'sample_count':len(x),'micro_batch_sizes':[4,4,3],
           'max_gradient_difference':abs_difference,
           'gradient_norm_before_clip':before,'gradient_norm_after_clip':after,
           'clip_max_norm':clip_max_norm}
    frame=pd.DataFrame({'parameter_index':np.arange(len(gradient_full)),
                        'full_batch_gradient':gradient_full.numpy(),
                        'micro_batch_gradient':gradient_micro.numpy(),
                        'clipped_gradient':clipped.numpy()})
    if output_dir is not None:
        import json
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        (out/'gradient_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
        frame.to_csv(out/'gradient_vectors.csv',index=False)
    return audit,frame

if __name__=='__main__':
    report,_=run(output_dir=Path(__file__).resolve().parents[1]/'outputs'/'advanced_02')
    print(report)
