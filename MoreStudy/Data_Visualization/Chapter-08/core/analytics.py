"""대시보드의 입력 검증, 집계, Figure 제작. UI를 호출하지 않는 순수 로직."""
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def read_retail(path=DATA_DIR/'retail_daily.csv'):
    df = pd.read_csv(path,parse_dates=['date'])
    required = {'date','store','category','quantity','unit_price_krw','revenue_krw'}
    if not required.issubset(df.columns):
        raise ValueError('Retail CSV에 필수 열이 누락되었습니다.')
    try:
        df['date']=pd.to_datetime(df['date'],format='%Y-%m-%d',errors='raise')
        for col in ['quantity','revenue_krw','unit_price_krw']:
            df[col]=pd.to_numeric(df[col],errors='raise')
    except (ValueError,TypeError) as exc:
        raise ValueError('날짜 또는 숫자 필드가 올바르지 않습니다.') from exc
    nums=df[['quantity','revenue_krw','unit_price_krw']]
    if nums.isna().any().any() or not np.isfinite(nums.to_numpy(dtype=float)).all():
        raise ValueError('숫자 열에 결측값 또는 무한대가 있습니다.')
    if (nums<0).any().any():
        raise ValueError('수량과 매출은 음수가 될 수 없습니다.')
    if not df['quantity'].mod(1).eq(0).all():
        raise ValueError('수량은 정수여야 합니다.')
    if not (df['quantity']*df['unit_price_krw']).eq(df['revenue_krw']).all():
        raise ValueError('수량×단가와 매출의 합계가 일치하지 않습니다.')
    return df


def read_service(path=DATA_DIR/'service_hourly.csv'):
    df=pd.read_csv(path,parse_dates=['timestamp_utc'])
    if not {'timestamp_utc','service','requests','errors','p95_ms'}.issubset(df.columns):
        raise ValueError('Service CSV 필수 열 누락')
    if (df[['requests','errors','p95_ms']]<0).any().any():
        raise ValueError('음수 관측값')
    if (df['errors']>df['requests']).any():
        raise ValueError('오류 건수가 요청 수보다 클 수 없습니다.')
    return df


def read_tickets(path=DATA_DIR/'tickets.csv'):
    df=pd.read_csv(path,parse_dates=['created_date'])
    if not {'ticket_id','created_date','team','priority','status','first_response_hours'}.issubset(df.columns):
        raise ValueError('Tickets CSV 필수 열 누락')
    if df['ticket_id'].duplicated().any() or (df['first_response_hours']<0).any():
        raise ValueError('문의 ID 중복 또는 음수 응답시간')
    return df


def select_dates(df,date_col,start,end):
    """양 끝 날짜를 포함한다. UTC 시각 열은 먼저 화면 표시 날짜로 변환할 것."""
    start=pd.Timestamp(start).date(); end=pd.Timestamp(end).date()
    if start>end:raise ValueError('시작 날짜는 종료 날짜보다 늦을 수 없습니다.')
    dates=pd.to_datetime(df[date_col]).dt.date
    return df.loc[dates.between(start,end)].copy()


def select_retail(df,stores=None,categories=None,start=None,end=None):
    result=df.copy()
    if stores is not None: result=result.loc[result['store'].isin(stores)]
    if categories is not None: result=result.loc[result['category'].isin(categories)]
    if start is not None and end is not None:result=select_dates(result,'date',start,end)
    return result.copy()


def retail_summary(df):
    return {'revenue_krw':int(df['revenue_krw'].sum()),
            'quantity':int(df['quantity'].sum()),
            'days':int(df['date'].dt.normalize().nunique()),
            'rows':len(df)}


def retail_charts(df):
    daily=df.groupby('date',as_index=False)['revenue_krw'].sum().sort_values('date')
    cats=df.groupby('category',as_index=False)['revenue_krw'].sum().sort_values('revenue_krw',ascending=False)
    trend=px.line(daily,x='date',y='revenue_krw',markers=True,title='Daily Revenue')
    trend.update_layout(xaxis_title='Date',yaxis_title='Revenue (KRW)')
    category=px.bar(cats,x='category',y='revenue_krw',title='Revenue by Category')
    category.update_layout(xaxis_title='Category',yaxis_title='Revenue (KRW)')
    return trend,category


def service_summary(df):
    n=int(df['requests'].sum());err=int(df['errors'].sum())
    return {'requests':n,'errors':err,'error_rate_pct':(err/n*100) if n else None,
            'max_hourly_p95_ms':float(df['p95_ms'].max()) if len(df) else None,
            'hours':int(df['timestamp_utc'].nunique())}


def service_charts(df):
    trend=px.line(df.sort_values('timestamp_utc'),x='timestamp_utc',y='p95_ms',color='service',title='Hourly P95 Latency')
    trend.update_layout(xaxis_title='UTC',yaxis_title='P95 (ms)')
    by_service=df.groupby('service',as_index=False)[['requests','errors']].sum()
    by_service['error_rate_pct']=by_service['errors'].div(by_service['requests'].where(by_service['requests']!=0)).mul(100)
    bars=px.bar(by_service,x='service',y='error_rate_pct',title='Error Rate by Service')
    bars.update_layout(xaxis_title='Service',yaxis_title='Error Rate (%)')
    return trend,bars


def ticket_summary(df):
    open_count=int(df['status'].eq('Open').sum()); total=len(df)
    return {'tickets':total,'open':open_count,'open_rate_pct':open_count/total*100 if total else None,
            'median_response_h':float(df['first_response_hours'].median()) if total else None}


def tickets_charts(df):
    df=df.copy();df['day']=df['created_date'].dt.normalize()
    daily=df.groupby(['day','status'],as_index=False).size().rename(columns={'size':'tickets'})
    trend=px.bar(daily,x='day',y='tickets',color='status',title='Tickets by Day')
    fig=px.box(df,x='team',y='first_response_hours',points='outliers',title='First Response by Team')
    return trend,fig


def as_csv_bytes(df):
    return df.to_csv(index=False).encode('utf-8-sig')


def parse_uploaded_retail(content,max_size=2_000_000):
    import io
    if not content or len(content)>max_size:raise ValueError('CSV 파일 크기를 확인하세요 (최대 2MB).')
    df=read_retail(io.BytesIO(content))
    if df.empty:raise ValueError('빈 CSV 파일입니다.')
    if len(df)>100_000:raise ValueError('입력 행 수 상한을 초과했습니다.')
    return df


def date_bounds(df,column):
    d=pd.to_datetime(df[column]);return d.min().date(),d.max().date()
