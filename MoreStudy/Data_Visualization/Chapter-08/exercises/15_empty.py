"""Coding Practice 15. 빈 선택 처리

상황: 매장 선택이 없으면 사용자 안내 후 실행을 중단하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/15_empty.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail
df=read_retail()
selected=st.multiselect('Stores',sorted(df['store'].unique()),default=[])
filtered=select_retail(df,stores=selected)
if filtered.empty:st.info('매장을 선택하세요.')  # TODO: 뒤쪽 계산 중단
st.dataframe(filtered.head(),hide_index=True)
