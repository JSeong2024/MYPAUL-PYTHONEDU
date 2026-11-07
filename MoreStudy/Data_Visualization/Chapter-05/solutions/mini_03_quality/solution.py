from pathlib import Path
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from project_utils.eda import validated_inspections,wilson_interval

def run(output=None,source=None):
    raw=pd.read_csv(source or ROOT/'data/inspections.csv')
    valid,dups=validated_inspections(raw)
    out=Path(output or ROOT/'output/mini_03_quality');out.mkdir(parents=True,exist_ok=True)
    group=valid.groupby(['plant','line'],as_index=False).agg(n=('is_defective','size'),defects=('is_defective','sum'),review_count=('measurement_review','sum'))
    group['defect_rate']=group['defects']/group['n']
    intervals=[wilson_interval(int(r.defects),int(r.n)) for r in group.itertuples()]
    group['low']=[v[0] for v in intervals];group['high']=[v[1] for v in intervals]
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    sns.barplot(data=group,x='line',y='defect_rate',hue='plant',ax=axes[0],errorbar=None)
    axes[0].set(ylabel='Defect share',title='Observed defect rates by line')
    order=valid[~valid.measurement_review].copy()
    sns.boxplot(data=order,x='plant',y='thickness_mm',ax=axes[1],color='#8BB2CF')
    axes[1].set(title='Thickness measurements (valid 8-12 mm)',ylabel='Thickness (mm)')
    fig.suptitle('Manufacturing Quality Exploration')
    fig.savefig(out/'report.png',dpi=140);plt.close(fig)
    group.to_csv(out/'line_summary.csv',index=False)
    result={'raw_count':len(raw),'deduplicated_count':len(valid),'duplicate_count':dups,'measurement_review_count':int(valid.measurement_review.sum())}
    (out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':print(run())
