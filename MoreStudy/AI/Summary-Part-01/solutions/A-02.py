"""A-02: time-ordered Ridge selection without validation/test leakage."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from common import read_csv, date_str, finite, integer, save_csv, regression_metrics

FEATURES=['temperature_c','occupants','is_weekend']; TARGET='consumption_m3'; ALPHAS=(0.1,1.0,10.0)


def load():
    df=read_csv('daily_water.csv',['date',*FEATURES,TARGET])
    if len(df)<30: raise ValueError('daily_water.csv: at least 30 rows required')
    if df['date'].duplicated().any() or any(date_str(d) is None for d in df['date']):
        raise ValueError('invalid/duplicate date')
    for c in FEATURES+[TARGET]:
        if c in ('occupants','is_weekend'):
            vals=[integer(v) for v in df[c]]
            if None in vals or (c=='is_weekend' and not set(vals)<={0,1}):
                raise ValueError(f'invalid {c}')
            df[c]=vals
        else:
            vals=[finite(v) for v in df[c]]
            if None in vals or (c==TARGET and any(v<0 for v in vals)):
                raise ValueError(f'invalid {c}')
            df[c]=vals
    return df.sort_values('date',kind='stable').reset_index(drop=True)


def model(alpha):
    return Pipeline([('scaler',StandardScaler()),('model',Ridge(alpha=alpha))])


def main():
    df=load(); n=len(df);a=int(n*.6);b=a+int(n*.2)
    tr,val,te=df.iloc[:a],df.iloc[a:b],df.iloc[b:]
    baseline=float(tr[TARGET].mean())
    comparison=[{'model':'baseline','validation_mae':f'{regression_metrics(val[TARGET],np.full(len(val),baseline))["mae"]:.4f}'}]
    experiments=[]
    for alpha in ALPHAS:
        fit=model(alpha).fit(tr[FEATURES],tr[TARGET])
        mae=regression_metrics(val[TARGET],fit.predict(val[FEATURES]))['mae']
        experiments.append((mae,alpha,fit))
        comparison.append({'model':f'alpha={alpha:.1f}','validation_mae':f'{mae:.4f}'})
    _,best_alpha,best_model=min(experiments,key=lambda x:(x[0],x[1]))
    predictions=best_model.predict(te[FEATURES]);actual=te[TARGET].to_numpy(dtype=float)
    m=regression_metrics(actual,predictions); baseline_m=regression_metrics(actual,np.full(len(te),baseline))
    save_csv('model_comparison.csv',comparison,['model','validation_mae'])
    pd.DataFrame({'date':te['date'].to_numpy(),'actual':actual,'predicted':predictions,'residual':actual-predictions}).to_csv('test_predictions.csv',index=False,float_format='%.4f',lineterminator='\n')
    verdict='MODEL' if m['mae']<baseline_m['mae'] else 'BASELINE' if m['mae']>baseline_m['mae'] else 'TIE'
    Path('report.txt').write_text(f'BEST_ALPHA {best_alpha:.1f}\nTEST_MAE {m["mae"]:.4f}\nTEST_RMSE {m["rmse"]:.4f}\nBASELINE_TEST_MAE {baseline_m["mae"]:.4f}\nBEST {verdict}\n',encoding='utf-8')


if __name__=='__main__':
    try: main()
    except ValueError as error: raise SystemExit(f'ERROR: {error}') from error
