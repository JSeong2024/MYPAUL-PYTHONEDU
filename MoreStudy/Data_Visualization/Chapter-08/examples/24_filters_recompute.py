"""Example 24. 필터에 따른 재계산. Run: streamlit run examples/24_filters_recompute.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,retail_summary,retail_charts
df=read_retail()
store=st.selectbox('Store',sorted(df['store'].unique()))
selected=select_retail(df,stores=[store])
metrics=retail_summary(selected)
st.metric('Selected revenue (KRW)',f"{metrics['revenue_krw']:,}")
fig,_=retail_charts(selected)
st.plotly_chart(fig,width='stretch')
st.caption('필터링을 먼저 수행한 다음 KPI와 Figure를 모두 재계산합니다.')
