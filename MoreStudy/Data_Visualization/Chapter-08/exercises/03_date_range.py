"""Coding Practice 03. 기간 선택

상황: 시작일·종료일을 선택하고 유효한 두 날짜가 있는지 검사하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/03_date_range.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail,date_bounds
df=read_retail();a,b=date_bounds(df,'date')
range_value = ()  # TODO: st.date_input()으로 날짜 범위 받기
if len(range_value)!=2:st.info('시작일과 종료일을 모두 선택하세요.');st.stop()
filtered=select_retail(df,start=range_value[0],end=range_value[1])
st.write('Rows:',len(filtered))
