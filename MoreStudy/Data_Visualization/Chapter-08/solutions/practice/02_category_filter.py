"""Coding Practice Reference Example 05. 복수 분류 필터. Run: streamlit run examples/05_multiselect.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail
df=read_retail();options=sorted(df['category'].unique())
chosen=st.multiselect('Categories', options,default=options)
filtered=select_retail(df,categories=chosen)
if filtered.empty:st.warning('선택한 분류에 기록이 없습니다.')
else:st.dataframe(filtered.head(20),hide_index=True)
