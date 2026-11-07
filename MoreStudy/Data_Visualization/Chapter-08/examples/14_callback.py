"""Example 14. Callback. Run: streamlit run examples/14_callback.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('Callback Counter')
if 'clicks' not in st.session_state:st.session_state.clicks=0
def increment():st.session_state.clicks+=1
st.button('Increment',on_click=increment)
st.write('Clicks:',st.session_state.clicks)
st.caption('Callback은 스크립트 본문 재실행 전에 호출됩니다.')
