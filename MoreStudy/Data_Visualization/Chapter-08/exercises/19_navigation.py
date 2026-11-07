"""Coding Practice 19. 두 페이지 메뉴

상황: Overview·Details 페이지를 Streamlit 네비게이션에 등록하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/19_navigation.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,retail_summary

def overview():
    st.title('Overview')
    st.metric('Revenue',f"{retail_summary(read_retail())['revenue_krw']:,} KRW")

def details():
    st.title('Details')
    st.dataframe(read_retail().head(20),hide_index=True)

page=None  # TODO: st.navigation([st.Page(...), st.Page(...)])
if page is not None:page.run()  # TODO 완료 후 페이지 실행
