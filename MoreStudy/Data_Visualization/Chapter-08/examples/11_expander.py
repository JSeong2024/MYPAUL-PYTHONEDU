"""Example 11. 보조 설명 접기. Run: streamlit run examples/11_expander.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.title('Data Notes')
st.write('현재 화면에는 일자별 매출이 표시됩니다.')
with st.expander('용어 설명'):
    st.write('Revenue: quantity × unit price. 누락 기록을 0원과 혼동하면 안 됩니다.')
