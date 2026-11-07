"""Coding Practice 13. 현재 테이블 내보내기

상황: UTF-8 CSV 다운로드 버튼을 구성하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/13_download.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_retail,as_csv_bytes
df=read_retail()
st.info('TODO: download_button과 CSV Bytes 연결')
st.caption('UTF-8 BOM을 포함해 일부 스프레드시트 환경에서 한글 호환성을 높였습니다.')
