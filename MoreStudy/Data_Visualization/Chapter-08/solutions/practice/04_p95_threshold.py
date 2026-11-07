"""Coding Practice Reference Example 07. 임계값 슬라이더. Run: streamlit run examples/07_slider.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_service
service=read_service(); threshold=st.slider('P95 threshold (ms)',100,500,250,10)
exceeded=service.loc[service['p95_ms']>threshold]
st.metric('Hourly records above threshold',len(exceeded))
st.caption('각 시간대의 P95를 비교하며 전체 요청의 P95가 아닙니다.')
