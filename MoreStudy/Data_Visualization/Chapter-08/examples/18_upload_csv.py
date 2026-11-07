"""Example 18. CSV Upload. Run: streamlit run examples/18_upload_csv.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import parse_uploaded_retail
uploaded=st.file_uploader('Upload retail CSV (2MB max)',type=['csv'])
if uploaded is None:st.info('CSV 파일을 선택하세요.')
else:
    try:
        df=parse_uploaded_retail(uploaded.getvalue())
        st.success(f'Valid rows: {len(df)}')
        st.dataframe(df.head(10),hide_index=True)
    except (ValueError,UnicodeError,KeyError) as exc:
        st.error(f'입력 검증 실패: {exc}')
