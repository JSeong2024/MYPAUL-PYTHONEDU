"""Coding Practice 12. 데이터 로딩 캐시

상황: 파일 변경 시 캐시 키가 바뀌도록 함수에 인수를 전달하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/12_cache.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,DATA_DIR
p=DATA_DIR/'retail_daily.csv'
@st.cache_data
def load_retail_cached(file_path,modified_ns):
    return read_retail(file_path)
df=load_retail_cached(p,0)  # TODO: 실제 파일 수정시각으로 교체
st.metric('Cached rows',len(df))
st.caption('파일 변경 시 수정시각 인수가 달라져 캐시 키가 변경됩니다.')
