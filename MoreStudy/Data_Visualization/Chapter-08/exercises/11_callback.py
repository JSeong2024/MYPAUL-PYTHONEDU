"""Coding Practice 11. Callback 구현

상황: 버튼 클릭 전에 실행되는 increment 콜백을 연결하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/11_callback.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('Callback Counter')
if 'clicks' not in st.session_state:st.session_state.clicks=0
def increment():st.session_state.clicks+=1
st.button('Increment')  # TODO: on_click 연결
st.write('Clicks:',st.session_state.clicks)
st.caption('Callback은 스크립트 본문 재실행 전에 호출됩니다.')
