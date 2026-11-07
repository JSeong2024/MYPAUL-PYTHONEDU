"""Mini 01: completed orders visualization report; synthetic educational data."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from project_utils.common import ROOT, DATA, theme, export, export_json

def prepare(data_path=DATA / "retail_orders.csv"):
    df = pd.read_csv(data_path, parse_dates=["date"])
    required = {"date","branch","category","channel","revenue_krw","status"}
    if not required.issubset(df.columns):
        raise ValueError(f"missing columns: {required - set(df.columns)}")
    if df["revenue_krw"].lt(0).any():
        raise ValueError("negative revenue")
    return df.query("status == 'Completed'").copy()

def summarize(df):
    if df.empty: raise ValueError("no completed orders")
    daily = df.groupby("date", as_index=False)["revenue_krw"].sum()
    branch = df.groupby("branch", as_index=False)["revenue_krw"].sum().sort_values("revenue_krw",ascending=False)
    category = df.groupby("category", as_index=False)["revenue_krw"].sum()
    return daily, branch, category

def run(output_dir=ROOT / "output" / "mini_01_retail", data_path=DATA / "retail_orders.csv"):
    theme(); df=prepare(data_path); daily, branch, category=summarize(df)
    fig, axes=plt.subplots(2,2,figsize=(12,8),layout="constrained")
    sns.lineplot(data=daily,x="date",y="revenue_krw",ax=axes[0,0],marker="o",errorbar=None)
    axes[0,0].set(title="Daily completed revenue",xlabel="Date",ylabel="Revenue (KRW)");axes[0,0].tick_params(axis="x",rotation=30)
    sns.barplot(data=branch,y="branch",x="revenue_krw",color="steelblue",errorbar=None,ax=axes[0,1])
    axes[0,1].set(title="Revenue by branch",xlabel="Revenue (KRW)",ylabel="Branch")
    sns.boxplot(data=df,x="channel",y="revenue_krw",color="lightblue",ax=axes[1,0])
    axes[1,0].set(title="Order value distribution",xlabel="Channel",ylabel="Completed order value (KRW)")
    sns.barplot(data=category,x="category",y="revenue_krw",color="steelblue",errorbar=None,ax=axes[1,1])
    axes[1,1].set(title="Revenue by product category",xlabel="Category",ylabel="Revenue (KRW)");axes[1,1].tick_params(axis="x",rotation=20)
    out=Path(output_dir);export(fig,out/"retail_report.png")
    daily.to_csv(out/"daily_revenue.csv",index=False)
    result={"completed_rows":int(len(df)),"total_revenue_krw":int(df.revenue_krw.sum()),"branches":int(df.branch.nunique())}
    export_json(result,out/"summary.json");return result
if __name__ == "__main__": print(run())
