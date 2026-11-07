"""Coding Practice Reference Example 13. Session State. Run: streamlit run examples/13_session_state.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('Session Counter')
if 'count' not in st.session_state:st.session_state['count']=0
if st.button('Add one'):st.session_state['count']+=1
if st.button('Reset'):st.session_state['count']=0
st.metric('Count this session',st.session_state['count'])
