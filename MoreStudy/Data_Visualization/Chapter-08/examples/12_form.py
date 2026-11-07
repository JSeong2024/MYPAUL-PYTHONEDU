"""Example 12. Form. Run: streamlit run examples/12_form.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,select_retail
df=read_retail();options=sorted(df['store'].unique())
with st.form('store_filter'):
    chosen=st.multiselect('Stores',options,default=options)
    submitted=st.form_submit_button('Apply')
if submitted:st.success('필터가 적용되었습니다.')
st.dataframe(select_retail(df,stores=chosen).head(12),hide_index=True)
st.caption('Form은 제출할 때 위젯 값을 함께 확정합니다.')
