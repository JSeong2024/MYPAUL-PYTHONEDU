"""Mini 02: latency distribution and threshold report."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from project_utils.common import ROOT, DATA, theme, export, export_json

LIMIT_MS=500

def prepare(path=DATA / "service_requests.csv"):
    df=pd.read_csv(path)
    required={"request_id","service","priority","response_ms","failed","hour"}
    if not required.issubset(df): raise ValueError("service schema mismatch")
    if df.request_id.duplicated().any() or df.response_ms.isna().any() or (df.response_ms <= 0).any():
        raise ValueError("invalid service request records")
    return df

def summarize(df):
    result=df.groupby("service").agg(requests=("request_id","count"), median_ms=("response_ms","median"),p95_ms=("response_ms",lambda x:float(x.quantile(.95))),over_limit=("response_ms",lambda x:int((x>LIMIT_MS).sum())))
    result["over_limit_rate_pct"]=result["over_limit"] / result["requests"]*100
    return result.reset_index()

def run(output_dir=ROOT/"output"/"mini_02_service",data_path=DATA/"service_requests.csv"):
    theme();df=prepare(data_path);agg=summarize(df);out=Path(output_dir)
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout="constrained")
    sns.boxplot(data=df,x="service",y="response_ms",color="lightblue",ax=axes[0,0]);axes[0,0].axhline(LIMIT_MS,ls="--",color="firebrick",label="500 ms limit");axes[0,0].legend();axes[0,0].set(title="Latency by service")
    sns.histplot(data=df,x="response_ms",hue="priority",binwidth=80,alpha=.55,ax=axes[0,1]);axes[0,1].set(title="Latency distribution",xlabel="Response (ms)")
    sns.barplot(data=agg,x="service",y="over_limit_rate_pct",color="steelblue",errorbar=None,ax=axes[1,0]);axes[1,0].set(title="Requests above 500 ms",ylabel="Share (%)")
    sns.scatterplot(data=agg,x="requests",y="p95_ms",hue="service",s=140,ax=axes[1,1]);axes[1,1].set(title="P95 latency vs volume",ylabel="P95 (ms)")
    export(fig,out/"service_report.png");agg.to_csv(out/"service_summary.csv",index=False)
    result={"requests":int(len(df)),"overall_median_ms":float(df.response_ms.median()),"over_limit":int((df.response_ms>LIMIT_MS).sum())}
    export_json(result,out/"summary.json");return result
if __name__=="__main__":print(run())
