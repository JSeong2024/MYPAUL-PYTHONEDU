"""Reference implementation: multi-station bicycle demand visualization.
Data is entirely synthetic. Requires station-level reporting coverage.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from project_utils.common import ROOT, DATA, theme, export, export_json
BANDS=['Morning','Afternoon','Evening']

def load_inputs(data_dir=DATA):
    p=Path(data_dir)
    rides=pd.read_csv(p/"bike_trips.csv", dtype={"station_id":"string"})
    stations=pd.read_csv(p/"bike_stations.csv",dtype={"station_id":"string"})
    reporting=pd.read_csv(p/"bike_reporting.csv",dtype={"station_id":"string"})
    if stations.station_id.isna().any() or stations.station_id.duplicated().any(): raise ValueError("duplicate/missing station ID")
    if reporting.duplicated(["date","station_id","time_band"]).any():raise ValueError("duplicate reporting slots")
    if not reporting.reporting.isin([0,1]).all():raise ValueError("reporting must be 0 or 1")
    if not set(reporting.station_id).issubset(set(stations.station_id)):raise ValueError("unknown station in reporting")
    if not set(reporting.time_band).issubset(BANDS):raise ValueError("unknown time band in reporting")
    reporting=reporting.copy()
    reporting["date"]=pd.to_datetime(reporting.date,format="%Y-%m-%d",errors="raise")
    return rides, stations, reporting

def clean_rides(rides,stations,reporting):
    df=rides.copy()
    date=pd.to_datetime(df.date,format="%Y-%m-%d",errors="coerce")
    duration=pd.to_numeric(df.duration_min,errors="coerce")
    valid_id=(df.ride_id.notna()) & (~df.ride_id.duplicated(keep="first"))
    valid_fields=date.notna() & df.station_id.isin(stations.station_id) & df.time_band.isin(BANDS) & duration.gt(0)&duration.le(240)&df.user_type.isin(['Member','Casual'])
    status_key=pd.MultiIndex.from_frame(reporting.loc[reporting.reporting.eq(1),["date","station_id","time_band"]])
    ride_key=pd.MultiIndex.from_arrays([date,df.station_id,df.time_band])
    valid=valid_id & valid_fields & ride_key.isin(status_key)
    accepted=df.loc[valid].copy();accepted["date"]=date.loc[valid];accepted["duration_min"]=duration.loc[valid]
    rejected=df.loc[~valid].copy();rejected["rejection_reason"]="invalid_or_unreported_record"
    return accepted,rejected

def build_slot_counts(accepted,reporting,stations):
    counts=accepted.groupby(["date","station_id","time_band"],as_index=False).size().rename(columns={"size":"rides"})
    if counts.duplicated(["date","station_id","time_band"]).any():raise ValueError("duplicate count key")
    slot=reporting.merge(counts,on=["date","station_id","time_band"],how="left",validate="one_to_one")
    slot["rides"]=slot["rides"].where(slot.reporting.eq(0),slot.rides.fillna(0))
    slot=slot.merge(stations,on="station_id",how="left",validate="many_to_one")
    if slot.station_name.isna().any():raise ValueError("unknown station")
    return slot

def filter_stations(slots,ids=None):
    if ids is None:return slots.copy()
    desired=list(ids)
    if not desired:raise ValueError("no stations selected")
    unknown=set(desired)-set(slots.station_id)
    if unknown:raise ValueError(f"unknown stations: {sorted(unknown)}")
    return slots.loc[slots.station_id.isin(desired)].copy()

def summarize(slots, accepted):
    names=slots.groupby("station_name",as_index=False).agg(observed_slots=("reporting","sum"),expected_slots=("reporting","size"),total_rides=("rides","sum"))
    names["coverage_pct"]=names.observed_slots/names.expected_slots*100
    grouped=slots.groupby(["station_name","time_band"],as_index=False).agg(avg_rides=("rides","mean"))
    daily=slots.groupby(["date","station_name"],as_index=False).agg(
        total_rides=("rides",lambda x:x.sum(min_count=1)),
        observed_slots=("reporting","sum"),
    )
    return names,grouped,daily

def run(output_dir=ROOT/"output"/"advanced_01_bike",data_dir=DATA,station_ids=None):
    theme();rides,stations,reporting=load_inputs(data_dir);accepted,rejected=clean_rides(rides,stations,reporting)
    slots=filter_stations(build_slot_counts(accepted,reporting,stations),station_ids)
    selected=set(slots.station_id);valid=accepted.loc[accepted.station_id.isin(selected)].copy()
    names,grouped,daily=summarize(slots,valid)
    if names.empty:raise ValueError("no selected stations")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    # Overall dashboard, no missing slot values interpreted as 0
    fig,axes=plt.subplots(2,2,figsize=(13,9),layout="constrained")
    sns.barplot(data=names.sort_values('total_rides',ascending=False),y="station_name",x="total_rides",color="steelblue",errorbar=None,ax=axes[0,0]);axes[0,0].set(title="Recorded rides by station",xlabel="Rides",ylabel="Station")
    sns.barplot(data=grouped,x="time_band",y="avg_rides",hue="station_name",order=BANDS,errorbar=None,ax=axes[0,1]);axes[0,1].set(title="Rides per observed time band",ylabel="Mean rides / reporting slot")
    axes[0,1].legend(fontsize=7,title=None)
    sns.histplot(data=valid,x="duration_min",bins=26,ax=axes[1,0],color="steelblue");axes[1,0].set(title="Trip duration",xlabel="Minutes")
    sns.barplot(data=names,y="station_name",x="coverage_pct",color="teal",errorbar=None,ax=axes[1,1]);axes[1,1].set(title="Data reporting coverage",xlabel="Reporting slots (%)",ylabel="Station",xlim=(0,105))
    export(fig,out/"bike_overview.png")
    hm=grouped.pivot(index="station_name",columns="time_band",values="avg_rides").reindex(columns=BANDS)
    fig,ax=plt.subplots(figsize=(8,max(3, .58*len(hm)+1)),layout="constrained")
    sns.heatmap(hm,annot=True,fmt=".1f",cmap="YlGnBu",ax=ax, cbar_kws={"label":"Mean rides per observed slot"})
    ax.set(title="Time band x station (observed only)");export(fig,out/"bike_heatmap.png")
    g=sns.relplot(data=daily,x="date",y="total_rides",col="station_name",col_wrap=3,kind="scatter",s=30,height=2.6,aspect=1.45)
    for name, ax in g.axes_dict.items():
        series=daily.loc[daily.station_name.eq(name)].sort_values("date")
        ax.plot(series["date"],series["total_rides"],color="steelblue",alpha=.6,linewidth=1.2)
    g.set_axis_labels("Date","Recorded rides");g.set_titles("{col_name}")
    for ax in g.axes.flat:ax.tick_params(axis="x",rotation=35)
    g.figure.suptitle("Daily recorded trips (see reporting coverage)",y=1.04)
    export(g.figure,out/"bike_station_facets.png")
    names.to_csv(out/"station_summary.csv",index=False);slots.to_csv(out/"reporting_slots.csv",index=False);rejected.to_csv(out/"rejected_rows.csv",index=False)
    result={"raw_ride_rows":int(len(rides)),"accepted_rides_all_stations":int(len(accepted)),"rejected_rows":int(len(rejected)),"selected_station_count":int(names.shape[0]),"selected_rides":int(len(valid)),"selected_reporting_slots":int(slots.reporting.sum()),"selected_expected_slots":int(len(slots))}
    export_json(result,out/"summary.json");return result
if __name__=="__main__":print(run())
