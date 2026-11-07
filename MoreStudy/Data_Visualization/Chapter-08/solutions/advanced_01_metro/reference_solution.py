"""Advanced reference implementation: Metro Operations Dashboard."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
import pandas as pd
from core.metro import (load_reference,load_raw,validate_metro,filter_metro,
                        metro_summary,metro_charts,missing_dates)
from core.analytics import as_csv_bytes
st.set_page_config(page_title='Metro Operations',layout='wide')

@st.cache_data
def load_builtin(raw_path,mtime):
    return load_raw(raw_path)

@st.cache_data
def validate_builtin(path,mtime,stations_json,policy_json):
    stations,policy=load_reference(path)
    raw=load_builtin(path/'metro_hourly_raw.csv',mtime)
    good,issues,coverage=validate_metro(raw,stations,policy)
    return stations,policy,good,issues,coverage

p=ROOT/'data';f=p/'metro_hourly_raw.csv'
stations,policy,good,issues,coverage=validate_builtin(p,f.stat().st_mtime_ns,
    (p/'stations.json').stat().st_mtime_ns,(p/'rail_policy.json').stat().st_mtime_ns)

st.sidebar.header('Metro Filters')
uploaded=st.sidebar.file_uploader('Optional raw CSV (max 3 MB)',type=['csv'])
if uploaded is not None:
    if uploaded.size>3_000_000:st.error('최대 3MB까지 업로드할 수 있습니다.');st.stop()
    try:
        import io
        raw=pd.read_csv(io.BytesIO(uploaded.getvalue()),dtype=str,keep_default_na=False,encoding='utf-8-sig')
        if len(raw)>100_000:raise ValueError('입력 행이 너무 많습니다.')
        good,issues,coverage=validate_metro(raw,stations,policy)
    except (ValueError,KeyError,UnicodeError,pd.errors.ParserError) as exc:
        st.error(f'CSV 검증 오류: {exc}');st.stop()

station_options=stations['station_id'].tolist()
if 'chosen_stations' not in st.session_state:
    st.session_state['chosen_stations']=station_options.copy()
# 이전에 다른 데이터를 사용했더라도 유효한 역만 유지
if not set(st.session_state['chosen_stations']).issubset(set(station_options)):
    st.session_state['chosen_stations']=station_options.copy()

if st.sidebar.button('Reset selected stations'):
    st.session_state['chosen_stations']=station_options.copy()
selected_stations=st.sidebar.multiselect('Stations',station_options,key='chosen_stations')
start=pd.Timestamp(policy['start_date']).date();end=pd.Timestamp(policy['end_date']).date()
period=st.sidebar.date_input('Date range',value=(start,end),min_value=start,max_value=end)
if len(period)!=2:
    st.info('시작 날짜와 종료 날짜를 모두 선택하세요.');st.stop()
if not selected_stations:
    st.info('역사를 하나 이상 선택하세요.');st.stop()
accepted,expected=filter_metro(good,coverage,selected_stations,*period)
summary=metro_summary(accepted,expected)


def overview():
    st.title('Metro Operations Overview')
    a,b,c,d=st.columns(4)
    a.metric('Boardings',f"{summary['boardings']:,}")
    b.metric('Accepted slots',f"{summary['accepted_slots']:,}")
    c.metric('Expected slots',f"{summary['expected_slots']:,}")
    d.metric('Coverage',f"{summary['coverage_pct']:.2f}%" if summary['coverage_pct'] is not None else 'N/A')
    st.caption('Boardings = station entries (not in-train occupancy). Missing slots are not zero boardings.')
    if accepted.empty:st.info('유효한 관측이 없습니다.');return
    daily,rank,heat=metro_charts(accepted,expected,stations)
    st.plotly_chart(daily,width='stretch')
    left,right=st.columns(2)
    with left:st.plotly_chart(rank,width='stretch')
    with right:st.plotly_chart(heat,width='stretch')


def quality():
    st.title('Data Quality')
    st.write('Raw invalid rows:',len(issues))
    st.metric('Missing or invalid slots (selected filters)',summary['missing_slots'])
    st.caption('Issue table below is the input-wide audit; selected-period coverage is shown separately.')
    daily=missing_dates(expected)
    st.dataframe(daily,hide_index=True)
    with st.expander('Excluded raw rows'):
        st.dataframe(issues,hide_index=True)


def exports():
    st.title('Exports')
    st.caption('CSV downloads follow the selected station and date filters.')
    st.download_button('Download accepted slots',as_csv_bytes(accepted),'metro_accepted_filtered.csv','text/csv')
    st.download_button('Download expected slots',as_csv_bytes(expected),'metro_expected_filtered.csv','text/csv')
    st.download_button('Download daily coverage',as_csv_bytes(missing_dates(expected)),
                       'metro_coverage_filtered.csv','text/csv')

page=st.navigation([st.Page(overview,title='Overview',default=True),
                    st.Page(quality,title='Data Quality'),st.Page(exports,title='Exports')])
page.run()
