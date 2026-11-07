"""Coding Practice Reference Example 21. Plotly Selection. Run: streamlit run examples/21_plotly_selection.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
import plotly.express as px
from core.analytics import read_retail
by=read_retail().groupby('store',as_index=False)['revenue_krw'].sum()
fig=px.bar(by,x='store',y='revenue_krw')
event=st.plotly_chart(fig,on_select='rerun',selection_mode='points',key='selected_bars')
selected=event.selection.points if event is not None else []
st.write('Selected points:',len(selected))
st.caption('선택한 점이 발생해도 별도 집계 로직이 없다면 KPI는 자동 변경되지 않습니다.')
