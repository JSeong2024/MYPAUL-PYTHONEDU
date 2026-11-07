"""Coding Practice 04. 시간별 P95 기준 초과

상황: 임계값 슬라이더를 만들고 초과 시간대 기록 수를 계산하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/04_p95_threshold.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
from core.analytics import read_service
service=read_service(); threshold = 250  # TODO: st.slider()로 조정 가능하게 만들기
exceeded=service.loc[service['p95_ms']>threshold]
st.metric('Hourly records above threshold',len(exceeded))
st.caption('각 시간대의 P95를 비교하며 전체 요청의 P95가 아닙니다.')
