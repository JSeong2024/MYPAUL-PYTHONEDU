"""Coding Practice 08. 설명 접기

상황: 추가 설명을 접을 수 있는 영역에 표시하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/08_expander.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('Data Notes')
st.write('현재 화면에는 일자별 매출이 표시됩니다.')
with st.expander('TODO: 용어 설명을 의미하는 제목'):
    st.write('Revenue: quantity × unit price. 누락 기록을 0원과 혼동하면 안 됩니다.')
