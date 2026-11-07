"""Example 06. 날짜 범위. Run: streamlit run examples/06_date_range.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,date_bounds
df=read_retail();a,b=date_bounds(df,'date')
range_value=st.date_input('Date range',value=(a,b),min_value=a,max_value=b)
if len(range_value)!=2:st.info('시작일과 종료일을 모두 선택하세요.');st.stop()
filtered=select_retail(df,start=range_value[0],end=range_value[1])
st.write('Rows:',len(filtered))
