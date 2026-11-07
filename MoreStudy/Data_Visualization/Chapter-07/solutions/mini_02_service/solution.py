"""Reference solution: Mini 02 — Service Latency Report."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from project_core.io import DATA, ROOT, export_html, export_json


def load_service(path: Path = DATA / "service_metrics.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"timestamp_utc", "service", "p95_latency_ms", "error_requests", "total_requests"}
    if not required.issubset(df):
        raise ValueError("필수 서비스 열 누락")
    df["timestamp_utc"] = pd.to_datetime(df.timestamp_utc, utc=True, errors="coerce")
    if df.timestamp_utc.isna().any():raise ValueError("잘못된 UTC 시각")
    if df.duplicated(["service","timestamp_utc"]).any():raise ValueError("중복 관측")
    if (df[["p95_latency_ms", "error_requests", "total_requests"]]<0).any().any():raise ValueError("음수 측정")
    if (df.error_requests>df.total_requests).any() or (df.total_requests==0).any():raise ValueError("잘못된 요청 수")
    return df.sort_values(["service","timestamp_utc"])


def make_figure(df:pd.DataFrame,threshold_ms:float=500.0) -> go.Figure:
    if threshold_ms<=0:raise ValueError("기준선은 양수")
    fig=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=.12,
                      subplot_titles=("15-min P95 Latency (ms)", "Errors / Requests (%)"))
    for service,g in df.groupby('service',sort=True):
        expected=pd.date_range(g.timestamp_utc.min(),g.timestamp_utc.max(),freq='15min',tz='UTC')
        g=g.set_index('timestamp_utc').reindex(expected)
        g.index.name='timestamp_utc'
        g=g.reset_index()
        fig.add_trace(go.Scatter(x=g.timestamp_utc,y=g.p95_latency_ms,name=service,mode='lines',connectgaps=False,
                                 legendgroup=service),row=1,col=1)
        fig.add_trace(go.Scatter(x=g.timestamp_utc,y=100*g.error_requests/g.total_requests,name=service,mode='lines',
                                 showlegend=False,legendgroup=service,connectgaps=False),row=2,col=1)
    fig.add_hline(y=threshold_ms,line_dash="dash",line_color="firebrick",row=1,col=1)
    fig.update_xaxes(rangeslider_visible=True,row=2,col=1)
    fig.update_layout(height=720,title="Service Reliability — Select Time Range",template="plotly_white",hovermode="x unified")
    fig.update_yaxes(title_text="P95 (ms)",row=1,col=1)
    fig.update_yaxes(title_text="Errors (%)",row=2,col=1)
    return fig


def run(output:Path=ROOT/'output/mini_02_service') ->dict:
    df=load_service()
    fig=make_figure(df)
    export_html(fig,output/'service_reliability.html')
    summary={"services":int(df.service.nunique()),"observations":int(len(df)),"max_p95_ms":float(df.p95_latency_ms.max())}
    export_json(summary,output/'summary.json')
    return summary


if __name__=='__main__':print(run())
