"""Coding Practice Reference Example 15. Cache Data. Run: streamlit run examples/15_cache_data.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,DATA_DIR
p=DATA_DIR/'retail_daily.csv'
@st.cache_data
def load_retail_cached(file_path,modified_ns):
    return read_retail(file_path)
df=load_retail_cached(p,p.stat().st_mtime_ns)
st.metric('Cached rows',len(df))
st.caption('파일 변경 시 수정시각 인수가 달라져 캐시 키가 변경됩니다.')
