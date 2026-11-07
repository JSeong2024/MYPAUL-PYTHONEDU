"""Mini Project starter — TODO 항목을 완성하세요."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
# TODO 1: core.analytics에서 데이터 로드 함수 import
st.title('Retail Sales Dashboard')
st.info('TODO: 필터 → 데이터 계산 → KPI → Plotly → 다운로드 순서로 완성하세요.')
# TODO 2: 사용자 필터를 sidebar 위젯으로 구성
# TODO 3: 필터된 데이터로 KPI와 Figure를 새로 계산
# TODO 4: 입력이 비어 있을 때 안전하게 처리
# TODO 5: 필터된 행을 CSV로 다운로드
