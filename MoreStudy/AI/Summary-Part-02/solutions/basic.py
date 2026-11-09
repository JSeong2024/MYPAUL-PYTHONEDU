"""Solutions for B-01 through B-05. Strict stdin contracts."""
import math
import sys
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

def parse_numbers(raw, n=None, integer=False):
    parts=raw.split()
    if n is not None and len(parts)!=n:raise ValueError('field count')
    values=[int(v) if integer else float(v) for v in parts]
    if not integer and any(not math.isfinite(v) for v in values):raise ValueError('nonfinite')
    return values

def read_matrix(lines, n, d):
    if len(lines)!=n:raise ValueError('row count')
    return [parse_numbers(line,d) for line in lines]

def b01(lines):
    n,d=parse_numbers(lines[0],2,True)
    if not 1<=n<=200 or not 1<=d<=20:raise ValueError('bounds')
    v=read_matrix(lines[1:],n,d)
    x=torch.tensor(v,dtype=torch.float32)
    if not torch.isfinite(x).all():raise ValueError('float32 overflow')
    s=x.sum(dim=0).tolist();m=x.mean(dim=1).tolist()
    return '\n'.join([f'SHAPE {n} {d}','DTYPE float32','COLUMN_SUM '+' '.join(f'{v:.2f}' for v in s),'ROW_MEAN '+' '.join(f'{v:.2f}' for v in m)])

def b02(lines):
    n,d=parse_numbers(lines[0],2,True)
    if not 1<=n<=200 or not 1<=d<=20:raise ValueError('bounds')
    if len(lines)!=3+n:raise ValueError('row count')
    offsets=parse_numbers(lines[1],d);scales=parse_numbers(lines[2],d)
    if any(v<=0 for v in scales):raise ValueError('scale')
    matrix=read_matrix(lines[3:],n,d)
    x=torch.tensor(matrix,dtype=torch.float64)
    y=(x+torch.tensor(offsets,dtype=torch.float64))*torch.tensor(scales,dtype=torch.float64)
    if not torch.isfinite(y).all():raise ValueError('overflow')
    rows=['SAMPLE_'+str(i+1)+' '+' '.join(f'{v:.2f}' for v in row) for i,row in enumerate(y.tolist())]
    return '\n'.join(rows+['CHANNEL_MEAN '+' '.join(f'{v:.2f}' for v in y.mean(dim=0).tolist())])

def b03(lines):
    if len(lines)!=1:raise ValueError('row count')
    w,b,x,y,eta=parse_numbers(lines[0],5)
    if not 0<eta<=1:raise ValueError('eta')
    w=torch.tensor(w,dtype=torch.float64,requires_grad=True);b=torch.tensor(b,dtype=torch.float64,requires_grad=True)
    prediction=w*x+b;loss=(prediction-y)**2;loss.backward()
    orig=[prediction.item(),loss.item(),w.grad.item(),b.grad.item()]
    with torch.no_grad():w-=eta*w.grad;b-=eta*b.grad;updated=(w*x+b).item()
    if not all(math.isfinite(v) for v in orig+[w.item(),b.item(),updated]):raise ValueError('overflow')
    return '\n'.join(f'{label} {value:.4f}' for label,value in zip(['PREDICTION','LOSS','GRAD_W','GRAD_B','UPDATED_W','UPDATED_B','UPDATED_PREDICTION'],orig+[w.item(),b.item(),updated]))

def b04(lines):
    if len(lines)!=1:raise ValueError('row count')
    n,d,h,o=parse_numbers(lines[0],4,True)
    if not 1<=n<=256 or any(not 1<=v<=128 for v in (d,h,o)):raise ValueError('bounds')
    model=nn.Sequential(nn.Linear(d,h),nn.ReLU(),nn.Linear(h,o))
    n1=sum(p.numel() for p in model[0].parameters());n2=sum(p.numel() for p in model[2].parameters())
    shape=tuple(model(torch.zeros(n,d)).shape)
    return '\n'.join([f'LAYER_1_PARAMETERS {n1}',f'LAYER_2_PARAMETERS {n2}',f'TOTAL_PARAMETERS {n1+n2}',f'OUTPUT_SHAPE {shape[0]} {shape[1]}'])

def b05(lines):
    if len(lines)!=2:raise ValueError('rows')
    n,b,drop=parse_numbers(lines[0],3,True)
    if not 1<=n<=200 or not 1<=b<=200 or drop not in (0,1):raise ValueError('header')
    ids=parse_numbers(lines[1],n,True)
    if len(set(ids))!=n:raise ValueError('duplicate')
    ds=TensorDataset(torch.tensor(ids,dtype=torch.long));loader=DataLoader(ds,batch_size=b,shuffle=False,drop_last=bool(drop))
    batches=[batch[0].tolist() for batch in loader]
    return '\n'.join([f'BATCHES {len(batches)}']+[f'BATCH_{i+1} '+' '.join(str(j) for j in row) for i,row in enumerate(batches)]+[f'DROPPED {n-sum(map(len,batches))}'])

def main(id):
    raw=sys.stdin.read()
    try:
        lines=raw.splitlines()
        if not lines:raise ValueError('empty')
        output=globals()[id.replace('-','').lower()](lines)
        print(output)
    except (ValueError,IndexError,TypeError,RuntimeError,OverflowError):
        print('INVALID')

if __name__=='__main__':main(sys.argv[1])
