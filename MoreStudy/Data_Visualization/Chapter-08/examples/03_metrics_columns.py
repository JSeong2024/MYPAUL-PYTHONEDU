"""Example 03. KPI와 레이아웃. Run: streamlit run examples/03_metrics_columns.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail, retail_summary
summary=retail_summary(read_retail())
st.title('Sales KPIs')
a,b,c=st.columns(3)
a.metric('Revenue (KRW)',f"{summary['revenue_krw']:,}")
b.metric('Items',f"{summary['quantity']:,}")
c.metric('Days',summary['days'])
