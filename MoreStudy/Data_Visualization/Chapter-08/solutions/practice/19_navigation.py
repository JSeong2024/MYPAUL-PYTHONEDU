"""Coding Practice Reference Example 23. Multipage Navigation. Run: streamlit run examples/23_navigation.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,retail_summary

def overview():
    st.title('Overview')
    st.metric('Revenue',f"{retail_summary(read_retail())['revenue_krw']:,} KRW")

def details():
    st.title('Details')
    st.dataframe(read_retail().head(20),hide_index=True)

page=st.navigation([st.Page(overview,title='Overview',default=True),st.Page(details,title='Details')])
page.run()
