"""Coding Practice 09. 제출 시 필터 반영

상황: 폼 안에 매장 선택을 만들고 제출 버튼을 지정하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/09_form.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail
df=read_retail();options=sorted(df['store'].unique())
with st.form('store_filter'):
    chosen=st.multiselect('Stores',options,default=options)
    submitted = False  # TODO: st.form_submit_button()
if submitted:st.success('필터가 적용되었습니다.')
st.dataframe(select_retail(df,stores=chosen).head(12),hide_index=True)
st.caption('Form은 제출할 때 위젯 값을 함께 확정합니다.')
