"""Coding Practice Reference Example 04. 단일 매장 필터. Run: streamlit run examples/04_selectbox.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,retail_summary
df=read_retail()
store=st.selectbox('Store',sorted(df['store'].unique()))
filtered=select_retail(df,stores=[store])
st.metric('Selected Store Revenue (KRW)',f"{retail_summary(filtered)['revenue_krw']:,}")
st.dataframe(filtered.head(10),hide_index=True)
