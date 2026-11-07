"""Mini Project reference solution."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_tickets,ticket_summary,tickets_charts,as_csv_bytes
st.set_page_config(page_title='Support Workload',layout='wide')
st.title('Customer Support Workload')
@st.cache_data
def load(path,mtime):return read_tickets(path)
p=ROOT/'data'/'tickets.csv';raw=load(p,p.stat().st_mtime_ns)
with st.sidebar:
    teams=sorted(raw['team'].unique());priorities=['Low','Normal','High','Urgent']
    selected_teams=st.multiselect('Teams',teams,default=teams)
    selected_pri=st.multiselect('Priorities',priorities,default=priorities)
filtered=raw.loc[raw['team'].isin(selected_teams)&raw['priority'].isin(selected_pri)].copy()
if filtered.empty:st.info('조건에 맞는 문의가 없습니다.');st.stop()
s=ticket_summary(filtered);a,b,c,d=st.columns(4)
a.metric('Tickets',s['tickets']);b.metric('Open',s['open'])
c.metric('Open rate',f"{s['open_rate_pct']:.1f}%")
d.metric('Median response',f"{s['median_response_h']:.2f} h")
afig,bfig=tickets_charts(filtered)
st.plotly_chart(afig,width='stretch')
st.plotly_chart(bfig,width='stretch')
with st.expander('지표 해석'):
    st.write('중앙값은 응답시간을 정렬했을 때 중앙에 있는 값입니다. 일부 긴 응답시간의 영향이 평균보다 적습니다.')
st.download_button('Export filtered tickets',as_csv_bytes(filtered),'tickets_filtered.csv','text/csv')
