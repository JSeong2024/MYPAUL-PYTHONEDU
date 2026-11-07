"""Coding Practice 14. 업로드 검증

상황: CSV 업로드 파일을 읽고 크기·내용 검증을 통과한 행만 표시하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/14_upload.py
"""
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
        df = None  # TODO: parse_uploaded_retail() 적용
        # TODO: df를 확인한 후 성공 메시지와 테이블 표시
    except (ValueError,UnicodeError,KeyError) as exc:
        st.error(f'입력 검증 실패: {exc}')
