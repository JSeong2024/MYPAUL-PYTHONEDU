"""Coding Practice 06. Matplotlib 보고서

상황: Figure를 표시하고 사용 후 닫아 자원을 관리하세요.
이 파일은 일부 미완성입니다. TODO를 완성한 뒤 Streamlit으로 실행하세요.
모범 구현: solutions/practice/06_mpl_view.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import streamlit as st
import matplotlib.pyplot as plt
from core.analytics import read_retail
df=read_retail();by=df.groupby('store')['revenue_krw'].sum().sort_values()
fig,ax=plt.subplots(figsize=(7,3.5))
ax.barh(by.index,by.values)
ax.set(xlabel='Revenue (KRW)',title='Revenue by Store')
fig.tight_layout()
st.info('TODO: st.pyplot(fig)로 그래프 표시')
# TODO: Figure 자원 정리
