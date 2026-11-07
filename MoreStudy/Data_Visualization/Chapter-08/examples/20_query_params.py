"""Example 20. URL Query Parameters. Run: streamlit run examples/20_query_params.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('URL State')
allowed=['Central','Riverside','Westgate','Harbor']
requested=st.query_params.get('store','Central')
if requested not in allowed:requested='Central'
selection=st.selectbox('Store',allowed,index=allowed.index(requested))
if selection!=st.query_params.get('store'):
    st.query_params['store']=selection
st.write('URL parameter:',selection)
st.caption('사용자가 조작한 URL 값은 반드시 허용 목록과 비교해야 합니다.')
