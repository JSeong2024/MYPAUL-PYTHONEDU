"""Coding Practice 20. 필터와 KPI 동기화

상황: 선택한 매장의 데이터를 먼저 필터링한 뒤 KPI와 Figure를 계산하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/20_recompute.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,retail_summary,retail_charts
df=read_retail()
store=st.selectbox('Store',sorted(df['store'].unique()))
selected=df.copy()  # TODO: 선택한 매장만 필터링
metrics=retail_summary(selected)
st.metric('Selected revenue (KRW)',f"{metrics['revenue_krw']:,}")
fig,_=retail_charts(selected)
st.plotly_chart(fig,width='stretch')
st.caption('필터링을 먼저 수행한 다음 KPI와 Figure를 모두 재계산합니다.')
