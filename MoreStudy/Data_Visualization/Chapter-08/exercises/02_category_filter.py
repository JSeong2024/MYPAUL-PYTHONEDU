"""Coding Practice 02. 상품 분류 선택

상황: 상품 분류를 하나 이상 선택하고 해당 범주만 테이블에 표시하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/02_category_filter.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail
df=read_retail();options=sorted(df['category'].unique())
chosen = []  # TODO: st.multiselect()로 분류 선택
filtered=select_retail(df,categories=chosen)
if filtered.empty:st.warning('선택한 분류에 기록이 없습니다.')
else:st.dataframe(filtered.head(20),hide_index=True)
