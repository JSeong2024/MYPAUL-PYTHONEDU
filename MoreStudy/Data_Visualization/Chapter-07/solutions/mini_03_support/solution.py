"""Reference solution: Mini 03 — Customer Support Response Explorer."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from project_core.io import DATA, ROOT, export_html, export_json


def load_tickets(path:Path=DATA/'support_tickets.csv') ->pd.DataFrame:
    df=pd.read_csv(path)
    required={'ticket_id','created_local','team','priority','first_response_min','status'}
    if not required.issubset(df):raise ValueError('문의 데이터 열 누락')
    if df.ticket_id.isna().any() or df.ticket_id.duplicated().any():raise ValueError('중복·결측 ID')
    df['first_response_min']=pd.to_numeric(df.first_response_min,errors='coerce')
    if df.first_response_min.isna().any() or (df.first_response_min<0).any():raise ValueError('잘못된 응답 시간')
    return df


def make_figures(df:pd.DataFrame):
    box=px.box(df,x='team',y='first_response_min',color='priority',points='outliers',
               category_orders={'priority':['Low','Normal','High']},title='Support Response Time Distribution',
               labels={'first_response_min':'First Response (min)'})
    box.update_layout(template='plotly_white')
    hist=px.histogram(df,x='first_response_min',color='team',nbins=35,
                      barmode='overlay',opacity=.65,title='Response Time Histogram')
    hist.update_layout(template='plotly_white')
    return box,hist


def run(output:Path=ROOT/'output/mini_03_support') ->dict:
    df=load_tickets()
    box,hist=make_figures(df)
    export_html(box,output/'team_boxplot.html')
    export_html(hist,output/'response_histogram.html')
    summary={'tickets':len(df),'median_first_response_min':float(df.first_response_min.median())}
    export_json(summary,output/'summary.json')
    return summary


if __name__=='__main__':print(run())
