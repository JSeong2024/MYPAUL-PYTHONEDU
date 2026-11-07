"""Coding Practice 18. 임계값 편집

상황: 사용자가 편집한 임계값에 음수·결측이 없는지 검증하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/18_editor.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
import pandas as pd
st.title('Threshold Editor')
settings=pd.DataFrame({'service':['API','Search','Checkout'],'threshold_ms':[230,290,380]})
changed=settings.copy()  # TODO: st.data_editor로 편집 가능하게 변경
if (pd.to_numeric(changed['threshold_ms'],errors='coerce')<=0).any() or pd.to_numeric(changed['threshold_ms'],errors='coerce').isna().any():
    st.error('임계값은 양수여야 합니다.')
else:st.success('현재 세션에서 검증 완료 (원본 CSV는 수정하지 않음)')
