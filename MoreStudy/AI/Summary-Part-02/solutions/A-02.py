"""A-02: MLP trained by fixed split, validation-accuracy-selected weights."""
import copy,sys
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import torch
from torch import nn
from common import args_or_default,setup,scale,make_mlp,train_epoch,predict,binary_scores,write_json

def main(argv=None):
 a=args_or_default(argv,'A-02');setup()
 df=pd.read_csv(a.data/'usage.csv');parts={k:df[df.split==k].copy() for k in ('train','validation','test')}
 f=['x1','x2'];train=parts['train'];v=parts['validation'];te=parts['test']
 tx,[vx,ex],mean,std=scale(train[f].to_numpy(),[v[f].to_numpy(),te[f].to_numpy()])
 x=torch.tensor(tx);y=torch.tensor(train[['crowded']].to_numpy(dtype='float32'))
 valx=torch.tensor(vx);valy=v.crowded.to_numpy();testx=torch.tensor(ex)
 model=make_mlp([2,12,1]);opt=torch.optim.AdamW(model.parameters(),lr=.01);criterion=nn.BCEWithLogitsLoss()
 best=-1;best_epoch=0;best_state=None;hist=[]
 for epoch in range(1,101):
  loss=train_epoch(model,opt,criterion,x,y,16,epoch)
  p=predict(model,valx,True);acc=float(accuracy_score(valy,(p>=.5).astype(int)))
  hist.append({'epoch':epoch,'train_loss':loss,'validation_accuracy':acc})
  if acc>best+1e-12:best=acc;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
 model.load_state_dict(best_state)
 probs=predict(model,testx,True);actual=te.crowded.to_numpy();scores=binary_scores(actual,probs)
 counts=train.crowded.value_counts();majority=0 if counts.get(0,0)>=counts.get(1,0) else 1
 pd.DataFrame(hist).to_csv(a.out/'training_history.csv',index=False)
 write_json(a.out/'model_selection.json',{'best_epoch':best_epoch,'best_validation_accuracy':best,'train_majority_class':majority,'test_baseline_accuracy':float(np.mean(actual==majority))})
 pd.DataFrame({'record_id':te.record_id,'actual':actual,'probability':[f'{v:.4f}' for v in probs],'predicted':(probs>=.5).astype(int)}).to_csv(a.out/'test_predictions.csv',index=False)
 write_json(a.out/'test_metrics.json',{k:scores[k] for k in ['accuracy','f1','tp','fp','fn','tn']})
if __name__=='__main__':main(sys.argv[1:])
