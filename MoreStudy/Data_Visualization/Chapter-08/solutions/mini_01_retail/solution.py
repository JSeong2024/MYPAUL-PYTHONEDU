"""Mini Project reference solution."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,retail_summary,retail_charts,as_csv_bytes,date_bounds
st.set_page_config(page_title='Retail Sales',layout='wide')
st.title('Retail Sales Dashboard')
@st.cache_data
def load_data(path,modified_ns):
    return read_retail(path)
p=ROOT/'data'/'retail_daily.csv'; df=load_data(p,p.stat().st_mtime_ns)
all_stores=sorted(df['store'].unique());all_cats=sorted(df['category'].unique())
with st.sidebar:
    st.header('Filters')
    stores=st.multiselect('Stores',all_stores,default=all_stores)
    cats=st.multiselect('Categories',all_cats,default=all_cats)
    lo,hi=date_bounds(df,'date')
    dates=st.date_input('Date range',value=(lo,hi),min_value=lo,max_value=hi)
if len(dates)!=2:st.info('시작일과 종료일을 선택하세요.');st.stop()
filtered=select_retail(df,stores=stores,categories=cats,start=dates[0],end=dates[1])
if filtered.empty:st.warning('선택한 조건에 해당하는 매출 데이터가 없습니다.');st.stop()
s=retail_summary(filtered); a,b,c=st.columns(3)
a.metric('Revenue (KRW)',f"{s['revenue_krw']:,}")
b.metric('Items',f"{s['quantity']:,}")
c.metric('Observed Days',s['days'])
trend,by_category=retail_charts(filtered)
left,right=st.columns(2)
with left:st.plotly_chart(trend,width='stretch')
with right:st.plotly_chart(by_category,width='stretch')
st.download_button('Export filtered CSV',as_csv_bytes(filtered),'retail_filtered.csv','text/csv')
