"""Coding Practice 17. Plotly 포인트 선택

상황: 막대그래프의 선택 이벤트를 받아 선택한 점 개수를 표시하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/17_selection.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
import plotly.express as px
from core.analytics import read_retail
by=read_retail().groupby('store',as_index=False)['revenue_krw'].sum()
fig=px.bar(by,x='store',y='revenue_krw')
event=st.plotly_chart(fig,key='selected_bars')  # TODO: on_select와 selection_mode
selected=event.selection.points if event is not None else []
st.write('Selected points:',len(selected))
st.caption('선택한 점이 발생해도 별도 집계 로직이 없다면 KPI는 자동 변경되지 않습니다.')
