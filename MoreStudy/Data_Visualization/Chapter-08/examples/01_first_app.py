"""Example 01. 첫 번째 웹 대시보드. Run: streamlit run examples/01_first_app.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.set_page_config(page_title='First Dashboard', layout='wide')
st.title('Store Snapshot')
st.write('Data Visualization Chapter 08')
st.info('Streamlit 앱은 터미널에서 streamlit run으로 시작합니다.')
