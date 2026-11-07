"""Coding Practice 16. URL 매장값 검증

상황: 허용 목록에 있는 매장만 URL 선택값으로 사용하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/16_query.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('URL State')
allowed=['Central','Riverside','Westgate','Harbor']
requested=st.query_params.get('store','Central')
# TODO: URL 매장값이 허용 목록에 없다면 안전한 기본값 지정
selection=st.selectbox('Store',allowed,index=allowed.index(requested) if requested in allowed else 0)
if selection!=st.query_params.get('store'):
    st.query_params['store']=selection
st.write('URL parameter:',selection)
st.caption('사용자가 조작한 URL 값은 반드시 허용 목록과 비교해야 합니다.')
