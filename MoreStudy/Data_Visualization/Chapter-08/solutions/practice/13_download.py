"""Coding Practice Reference Example 17. CSV Download. Run: streamlit run examples/17_download_button.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,as_csv_bytes
df=read_retail()
st.download_button('Download retail CSV',data=as_csv_bytes(df),file_name='retail_export.csv',mime='text/csv')
st.caption('UTF-8 BOM을 포함해 일부 스프레드시트 환경에서 한글 호환성을 높였습니다.')
