"""A-03: fair comparison of two (optimizer, learning rate) configurations."""
import copy,sys
import pandas as pd
import torch
from torch import nn
from common import args_or_default,setup,scale,make_mlp,train_epoch,predict,reg_scores,write_json

def main(argv=None):
 a=args_or_default(argv,'A-03');setup();df=pd.read_csv(a.data/'energy.csv')
 f=['occupancy','temperature_c','weekend'];train,val,test=[df[df.split==k].copy() for k in ('train','validation','test')]
 tx,[vx,ex],_,_=scale(train[f].to_numpy(),[val[f].to_numpy(),test[f].to_numpy()])
 x=torch.tensor(tx);y=torch.tensor(train[['energy_kwh']].to_numpy(dtype='float32'));xx=torch.tensor(vx);yy=val.energy_kwh.to_numpy();testx=torch.tensor(ex)
 initial=copy.deepcopy(make_mlp([3,16,1]).state_dict());hist=[];comps={};states={}
 configs={'A':('SGD',.02),'B':('AdamW',.01)}
 for name,(optname,lr) in configs.items():
  model=make_mlp([3,16,1]);model.load_state_dict(copy.deepcopy(initial))
  opt=torch.optim.SGD(model.parameters(),lr=lr,momentum=.9) if name=='A' else torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=.01)
  best=float('inf');be=0;bs=None
  for epoch in range(1,31):
   loss=train_epoch(model,opt,nn.MSELoss(),x,y,16,epoch)
   rmse=reg_scores(yy,predict(model,xx))['rmse'];hist.append({'candidate':name,'epoch':epoch,'train_loss':loss,'validation_rmse':rmse})
   if rmse<best-1e-12:best=rmse;be=epoch;bs=copy.deepcopy(model.state_dict())
  comps[name]={'optimizer':optname,'learning_rate':lr,'best_epoch':be,'best_validation_rmse':best};states[name]=bs
 selected='A' if comps['A']['best_validation_rmse']<=comps['B']['best_validation_rmse'] else 'B'
 final=make_mlp([3,16,1]);final.load_state_dict(states[selected]);pred=predict(final,testx)
 pd.DataFrame(hist).to_csv(a.out/'training_history.csv',index=False)
 write_json(a.out/'comparison.json',{'candidates':comps,'selected_candidate':selected})
 pd.DataFrame({'record_id':test.record_id,'actual':test.energy_kwh,'predicted':pred}).to_csv(a.out/'test_predictions.csv',index=False)
 write_json(a.out/'test_metrics.json',reg_scores(test.energy_kwh,pred))
if __name__=='__main__':main(sys.argv[1:])
