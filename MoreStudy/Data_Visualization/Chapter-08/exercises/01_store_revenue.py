"""Coding Practice 01. 매장별 매출 확인

상황: 매장 선택 위젯을 만들고 선택한 매장의 매출을 다시 계산하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/01_store_revenue.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,retail_summary
df=read_retail()
store = None  # TODO: st.selectbox()로 하나의 매장 선택
filtered=select_retail(df,stores=[store])
st.metric('Selected Store Revenue (KRW)',f"{retail_summary(filtered)['revenue_krw']:,}")
st.dataframe(filtered.head(10),hide_index=True)
