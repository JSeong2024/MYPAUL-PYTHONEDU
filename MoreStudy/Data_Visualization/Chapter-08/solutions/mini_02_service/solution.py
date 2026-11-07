"""Mini Project reference solution."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_service,service_summary,service_charts
st.set_page_config(page_title='Service Monitoring',layout='wide')
st.title('Service Latency Monitoring')
@st.cache_data
def load(path,mtime):return read_service(path)
p=ROOT/'data'/'service_hourly.csv';raw=load(p,p.stat().st_mtime_ns)
services=sorted(raw['service'].unique())
with st.sidebar:
    selected=st.multiselect('Services',services,default=services)
    threshold=st.slider('P95 threshold (ms)',100,500,260,10)
filtered=raw.loc[raw['service'].isin(selected)].copy()
if filtered.empty:st.warning('서비스를 하나 이상 선택해 주세요.');st.stop()
summary=service_summary(filtered);exceeded=int(filtered['p95_ms'].gt(threshold).sum())
a,b,c,d=st.columns(4)
a.metric('Requests',f"{summary['requests']:,}")
b.metric('Errors',f"{summary['errors']:,}")
c.metric('Error rate',f"{summary['error_rate_pct']:.2f}%" if summary['error_rate_pct'] is not None else "N/A")
d.metric('Hours above threshold',exceeded)
st.caption('P95는 시간대별 P95입니다. 이를 평균내 전체 요청의 P95로 해석할 수 없습니다.')
afig,bfig=service_charts(filtered)
st.plotly_chart(afig,width='stretch')
st.plotly_chart(bfig,width='stretch')
