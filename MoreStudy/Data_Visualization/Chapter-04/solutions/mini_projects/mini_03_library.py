"""Mini 03: library traffic and missing-date reporting."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from project_utils.common import ROOT,DATA,theme,export,export_json

def prepare(path=DATA/"library_visits.csv"):
    df=pd.read_csv(path,parse_dates=["date"])
    if df.duplicated(["branch","date"]).any():raise ValueError("duplicate branch/date")
    if df[["visitors","new_members","open_hours"]].isna().any().any() or (df[["visitors","new_members","open_hours"]]<0).any().any():raise ValueError("missing or negative values")
    return df

def build_calendar(df):
    dates=pd.date_range(df.date.min(),df.date.max(),freq="D")
    idx=pd.MultiIndex.from_product([sorted(df.branch.unique()), dates],names=["branch","date"])
    result=df.set_index(["branch","date"]).reindex(idx).reset_index()
    result["observed"]=result.visitors.notna()
    return result

def run(output_dir=ROOT/"output"/"mini_03_library",data_path=DATA/"library_visits.csv"):
    theme();df=prepare(data_path); calendar=build_calendar(df);out=Path(output_dir)
    g=sns.relplot(data=calendar,x="date",y="visitors",col="branch",col_wrap=2,kind="scatter",s=38,height=3,aspect=1.45)
    for branch, ax in g.axes_dict.items():
        series=calendar.loc[calendar.branch.eq(branch)].sort_values("date")
        # Preserve missing days: Matplotlib breaks the line at NaN.
        ax.plot(series["date"],series["visitors"],color="steelblue",alpha=.6,linewidth=1.4)
    g.set_axis_labels("Date","Visitors");g.set_titles("{col_name}")
    for ax in g.axes.flat:ax.tick_params(axis="x",rotation=35)
    g.figure.suptitle("Observed daily library visitors (gaps are missing)",y=1.04)
    export(g.figure,out/"library_facets.png")
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout="constrained")
    sns.barplot(data=df,x="branch",y="visitors",estimator="mean",errorbar=None,color="steelblue",ax=axes[0]);axes[0].set(title="Mean observed daily visitors",ylabel="Visitors")
    sns.scatterplot(data=df,x="visitors",y="new_members",hue="branch",ax=axes[1]);axes[1].set(title="Visitors and registrations")
    export(fig,out/"library_summary.png")
    report={"recorded_days":int(len(df)),"expected_days":int(len(calendar)),"missing_records":int((~calendar.observed).sum()),"total_observed_visitors":int(df.visitors.sum())}
    calendar.to_csv(out/"full_calendar.csv",index=False)
    export_json(report,out/"summary.json");return report
if __name__=="__main__":print(run())
