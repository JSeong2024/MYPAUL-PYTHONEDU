"""Advanced Project starter."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
st.set_page_config(page_title='Metro Operations',layout='wide')
st.title('Urban Metro Operations Dashboard')
st.info('TODO: 검증 → 완전한 시간 슬롯 → 사용자 필터 → 다중 페이지 → CSV 내보내기')
# TODO 1: 데이터 로드 및 스키마 검사
# TODO 2: 중복 행을 포함한 오류 검출과 관측 완전성 계산
# TODO 3: 역사/기간 위젯 생성 및 빈 선택 처리
# TODO 4: Overview, Data Quality, Exports 페이지 구현
# TODO 5: 선택값 유지, 내보내기, 경계 조건 검증
