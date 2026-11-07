"""Coding Practice 07. 두 그래프를 탭으로 구성

상황: 매출 추이와 분류 그래프를 별도 탭으로 표시하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/07_tabs.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,retail_charts
df=read_retail();trend,cat=retail_charts(df)
a,b=st.tabs(['TODO Trend','TODO Categories'])  # TODO: 알맞은 탭 제목
with a:st.plotly_chart(trend,width='stretch')
with b:st.plotly_chart(cat,width='stretch')
