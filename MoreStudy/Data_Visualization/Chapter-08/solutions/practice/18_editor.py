"""Coding Practice Reference Example 22. Data Editor. Run: streamlit run examples/22_data_editor.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
import pandas as pd
st.title('Threshold Editor')
settings=pd.DataFrame({'service':['API','Search','Checkout'],'threshold_ms':[230,290,380]})
changed=st.data_editor(settings,hide_index=True,num_rows='fixed')
if (pd.to_numeric(changed['threshold_ms'],errors='coerce')<=0).any() or pd.to_numeric(changed['threshold_ms'],errors='coerce').isna().any():
    st.error('임계값은 양수여야 합니다.')
else:st.success('현재 세션에서 검증 완료 (원본 CSV는 수정하지 않음)')
