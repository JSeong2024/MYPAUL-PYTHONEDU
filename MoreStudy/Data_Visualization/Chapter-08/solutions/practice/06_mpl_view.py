"""Coding Practice Reference Example 09. Matplotlib 연결. Run: streamlit run examples/09_matplotlib.py"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import streamlit as st
import matplotlib.pyplot as plt
from core.analytics import read_retail
df=read_retail();by=df.groupby('store')['revenue_krw'].sum().sort_values()
fig,ax=plt.subplots(figsize=(7,3.5))
ax.barh(by.index,by.values)
ax.set(xlabel='Revenue (KRW)',title='Revenue by Store')
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
