"""Coding Practice 10. 세션별 카운터

상황: 세션 상태를 초기화하고, Add one 버튼 클릭 시 값이 1 증가하도록 나머지 코드를 완성하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/10_state_counter.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('Session Counter')
if 'count' not in st.session_state:st.session_state['count']=0
if st.button('Add one'):pass  # TODO: count를 1 증가
if st.button('Reset'):st.session_state['count']=0
st.metric('Count this session',st.session_state['count'])
