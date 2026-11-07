"""Example 16. Cache Resource. Run: streamlit run examples/16_cache_resource.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
import re
@st.cache_resource
def compile_id_pattern():
    return re.compile(r'^TK-\d{4}$')
pattern=compile_id_pattern()
text=st.text_input('Ticket ID','TK-0001')
st.write('Valid:',bool(pattern.fullmatch(text)))
st.caption('공유 객체는 변경하지 않는다는 원칙을 지키세요.')
