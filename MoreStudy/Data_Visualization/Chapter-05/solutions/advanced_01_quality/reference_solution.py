from pathlib import Path
import argparse,json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from project_utils.eda import validated_inspections,bootstrap_mean_ci,wilson_interval

COLUMNS=['inspection_id','plant','line','shift','thickness_mm','is_defective']

def prepare_data(source):
    source=Path(source)
    if not source.is_file(): raise FileNotFoundError(source)
    raw=pd.read_csv(source)
    data,duplicates=validated_inspections(raw)
    if data.empty: raise ValueError('유효한 검사 기록이 없습니다.')
    if data['plant'].isna().any() or data['line'].isna().any():raise ValueError('소속 정보에 결측이 있습니다.')
    return data,duplicates

def summarize(data):
    result=data.groupby(['plant','line'],as_index=False).agg(n=('is_defective','size'),defects=('is_defective','sum'),measurement_review=('measurement_review','sum'))
    result['defect_rate']=result.defects/result.n
    ci=[wilson_interval(int(r.defects),int(r.n)) for r in result.itertuples()]
    result['rate_ci_low']=[c[0] for c in ci];result['rate_ci_high']=[c[1] for c in ci]
    return result

def render_plant(plant_data, name, destination):
    summary=summarize(plant_data)
    fig,axs=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    lines=summary.line.tolist()
    axs[0,0].bar(lines,summary.defect_rate,color='#588DAF')
    yerr=np.vstack([summary.defect_rate-summary.rate_ci_low,summary.rate_ci_high-summary.defect_rate])
    axs[0,0].errorbar(lines,summary.defect_rate,yerr=yerr,fmt='none',capsize=3,ecolor='#222222')
    axs[0,0].set(ylim=(0,min(1,max(.25,float(summary.rate_ci_high.max())*1.15))),ylabel='Defect share',title='Defect rate and Wilson interval')
    sns.countplot(data=plant_data,x='shift',hue='is_defective',ax=axs[0,1])
    axs[0,1].set(title='Observed checks by shift',ylabel='Count')
    proper=plant_data.loc[~plant_data.measurement_review]
    if not proper.empty:
        sns.boxplot(data=proper,x='line',y='thickness_mm',ax=axs[1,0],color='#80B2A0')
    axs[1,0].set(title='Thickness (8–12 mm)',ylabel='Millimeters')
    reviewed=plant_data.groupby('line',as_index=False)['measurement_review'].sum()
    axs[1,1].bar(reviewed.line,reviewed.measurement_review,color='#C18B60')
    axs[1,1].set(ylabel='Records',title='Measurement review count')
    fig.suptitle(f'{name} — Quality EDA Report')
    fig.savefig(destination,dpi=140);plt.close(fig)

def run(source=None,output=None,plants=None,seed=41):
    source=source or ROOT/'data/inspections.csv';out=Path(output or ROOT/'output/advanced_01_quality');out.mkdir(parents=True,exist_ok=True)
    data,duplicate_count=prepare_data(source)
    chosen=sorted(set(plants)) if plants else sorted(data.plant.unique())
    if not chosen: raise ValueError('플랜트를 1개 이상 선택하세요.')
    unknown=set(chosen)-set(data.plant.unique())
    if unknown: raise ValueError(f'선택 플랜트가 존재하지 않습니다: {sorted(unknown)}')
    subset=data[data.plant.isin(chosen)].copy()
    groups=summarize(subset)
    per_plant=[]
    for n,plant in enumerate(chosen):
        group=subset[subset.plant.eq(plant)]
        measured=group.loc[~group.measurement_review,'thickness_mm'].to_numpy()
        low,high=bootstrap_mean_ci(measured,seed=seed+n)
        render_plant(group,plant,out/f'{plant}.png')
        per_plant.append({'plant':plant,'n':int(len(group)),'defects':int(group.is_defective.sum()),'defect_rate':float(group.is_defective.mean()),'valid_thickness_n':int(len(measured)),'thickness_mean_ci':[low,high]})
    groups.to_csv(out/'line_summary.csv',index=False)
    result={'input_rows':int(len(pd.read_csv(source))),'duplicate_ids':duplicate_count,'selected_plants':chosen,'selected_rows':len(subset),'measurement_review_count':int(subset.measurement_review.sum()),'plants':per_plant,'limitations':'가상 검사 표본이며 인과·전체 생산량 추정 불가'}
    (out/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Quality EDA report generator')
    parser.add_argument('--input',default=str(ROOT/'data/inspections.csv'))
    parser.add_argument('--output',default=str(ROOT/'output/advanced_01_quality'))
    parser.add_argument('--plants',nargs='*')
    args=parser.parse_args();result=run(args.input,args.output,args.plants)
    print('selected plants:',result['selected_plants'],'rows:',result['selected_rows'])
