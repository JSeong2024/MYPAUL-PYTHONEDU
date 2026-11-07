"""Coding Practice 05. Plotly 그래프 연결

상황: 준비한 Figure를 Streamlit에 표시하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/05_plotly_sales.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,retail_charts
df=read_retail();fig,_=retail_charts(df)
st.title('Interactive Sales Trend')
st.info('TODO: st.plotly_chart()로 fig 표시')
