"""Example 02. 테이블 표시. Run: streamlit run examples/02_dataframe.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail
df=read_retail()
st.title('Retail Records')
st.caption('한 행 = 날짜 × 매장 × 상품 분류')
st.dataframe(df.head(25), hide_index=True)
