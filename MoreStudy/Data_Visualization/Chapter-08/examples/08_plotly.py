"""Example 08. Plotly 연결. Run: streamlit run examples/08_plotly.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,retail_charts
df=read_retail();fig,_=retail_charts(df)
st.title('Interactive Sales Trend')
st.plotly_chart(fig,width='stretch')
