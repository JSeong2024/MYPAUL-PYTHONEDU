"""Example 19. 빈 결과 처리. Run: streamlit run examples/19_empty_state.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail
df=read_retail()
selected=st.multiselect('Stores',sorted(df['store'].unique()),default=[])
filtered=select_retail(df,stores=selected)
if filtered.empty:st.info('매장을 하나 이상 선택하면 그래프를 표시합니다.');st.stop()
st.dataframe(filtered.head(),hide_index=True)
