"""Coding Practice Reference Example 10. Tabs. Run: streamlit run examples/10_tabs.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,retail_charts
df=read_retail();trend,cat=retail_charts(df)
a,b=st.tabs(['Daily Trend','Category Breakdown'])
with a:st.plotly_chart(trend,width='stretch')
with b:st.plotly_chart(cat,width='stretch')
