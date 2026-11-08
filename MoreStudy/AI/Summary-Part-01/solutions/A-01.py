"""A-01: choose threshold on validation scores only, then evaluate test once."""
import pandas as pd
from common import read_csv, finite, integer, metric, save_csv


def load(name):
    df=read_csv(name,['record_id','actual','score'])
    if df.empty: raise ValueError(f'{name}: no samples')
    if df['record_id'].eq('').any() or df['record_id'].duplicated().any():
        raise ValueError(f'{name}: missing or duplicate record_id')
    for i,row in df.iterrows():
        actual=integer(row['actual']); score=finite(row['score'])
        if actual not in (0,1) or score is None or not 0<=score<=1:
            raise ValueError(f'{name}: invalid actual/score at CSV line {i+2}')
    df['actual']=df['actual'].astype(int); df['score']=df['score'].astype(float)
    return df


def evaluate(df,threshold):
    return metric(df['actual'],(df['score']>=threshold).astype(int))


def main():
    val=load('validation_scores.csv');test=load('test_scores.csv')
    candidates=[0.30,0.50,0.70]
    scores=[evaluate(val,th)['f1'] for th in candidates]
    best=max(range(3),key=lambda i:(scores[i],candidates[i]))
    save_csv('threshold_report.csv',[{'threshold':f'{th:.2f}','validation_f1':f'{s:.4f}','selected':str(i==best)} for i,(th,s) in enumerate(zip(candidates,scores))],['threshold','validation_f1','selected'])
    m=evaluate(test,candidates[best])
    lines=[f'THRESHOLD {candidates[best]:.4f}',*(f'{k.upper()} {m[k]}' for k in ('tp','fp','fn','tn')),
           *(f'{key.upper()} {m[key]:.4f}' for key in ('precision','recall','f1'))]
    from pathlib import Path
    Path('test_report.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':
    try: main()
    except (ValueError,FileNotFoundError) as error:
        raise SystemExit(f'ERROR: {error}') from error
