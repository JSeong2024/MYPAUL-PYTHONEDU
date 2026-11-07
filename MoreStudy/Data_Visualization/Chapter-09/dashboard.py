"""Optional Streamlit capstone explorer for Chapter 09 (requires Streamlit).

Run: python -m streamlit run dashboard.py
Data is synthetic. The dashboard is descriptive, not a live operational service.
"""
from __future__ import annotations
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

st.set_page_config(page_title='Data Visualization Capstone',layout='wide')
st.title('Data Visualization — Capstone Explorer')
st.caption('Synthetic educational datasets · no live operational data')

@st.cache_data(show_spinner=False)
def get_dataset(choice):
    return {
        'Weather':weather_summary,
        'Retail':retail_summary,
        'Services':latency_summary,
        'Electricity':electricity_summary,
        'Metro':metro_summary,
        'Transit':transit_summary,
    }[choice]()

choice=st.sidebar.selectbox('Dataset',['Weather','Retail','Services','Electricity','Metro','Transit'])
result=get_dataset(choice)
if choice=='Weather':
    good,bad,daily,slots=result
    options=sorted(daily.region.unique())
    chosen=st.sidebar.multiselect('Regions',options,default=options)
    filtered=daily[daily.region.isin(chosen)].copy()
    st.metric('Selected daily aggregates',len(filtered))
    st.plotly_chart(px.line(filtered,x='date',y='temperature_c',color='region',title='Daily Mean Temperature (C)'),use_container_width=True)
    st.metric('Valid selected observations',len(good[good.region.isin(chosen)]))
    st.dataframe(filtered)
elif choice=='Retail':
    good,daily=result
    options=sorted(daily.store_id.unique())
    chosen=st.sidebar.multiselect('Stores',options,default=options)
    filtered=daily[daily.store_id.isin(chosen)].copy()
    st.metric('Completed revenue (KRW)',f'{int(filtered.revenue_krw.sum()):,}')
    st.plotly_chart(px.line(filtered,x='date',y='revenue_krw',color='store_id',title='Daily Completed Revenue (KRW)'),use_container_width=True)
    st.dataframe(filtered)
elif choice=='Services':
    good,summary=result
    options=summary.service.tolist()
    chosen=st.sidebar.multiselect('Services',options,default=options)
    filtered=good[good.service.isin(chosen)].copy()
    if not filtered.empty:
        report=filtered.groupby('service',as_index=False).agg(median_ms=('latency_ms','median'),p95_ms=('latency_ms',lambda s:s.quantile(.95)),error_rate=('is_error','mean'))
        st.plotly_chart(px.bar(report,x='service',y='p95_ms',title='P95 latency (ms)'),use_container_width=True)
        st.dataframe(report)
    else:st.info('Select at least one service.')
elif choice=='Electricity':
    good,bad,daily=result
    options=sorted(good.region.unique())
    chosen=st.sidebar.multiselect('Regions',options,default=options)
    filtered=good[good.region.isin(chosen)].copy()
    st.metric('Valid measurements',len(filtered))
    st.plotly_chart(px.line(filtered,x='timestamp_kst',y='demand_mw',color='region',title='Power Demand (MW, KST)'),use_container_width=True)
    st.dataframe(filtered[['region','timestamp_kst','demand_mw']])
elif choice=='Metro':
    good,bad,daily,slots=result
    options=sorted(daily.station_name.unique())
    chosen=st.sidebar.multiselect('Stations',options,default=options)
    filtered=daily[daily.station_name.isin(chosen)].copy()
    st.metric('Validated boardings (persons)',f'{int(filtered.boardings.sum()):,}')
    st.plotly_chart(px.line(filtered,x='date',y='boardings',color='station_name',title='Daily Boardings'),use_container_width=True)
    st.dataframe(filtered)
else:
    good,bad,daily,slots,incidents=result
    options=sorted(good.stop_id.unique())
    chosen=st.sidebar.multiselect('Stops',options,default=options)
    filtered=good[good.stop_id.isin(chosen)].copy()
    selected_slots=slots[slots.stop_id.isin(chosen)]
    st.metric('Validated boardings (persons)',f'{int(filtered.boardings.sum()):,}')
    st.metric('Expected slot coverage',f'{selected_slots.available.mean():.2%}' if len(selected_slots) else 'No stops selected')
    grouped=filtered.groupby('stop_id',as_index=False).agg(boardings=('boardings','sum'))
    st.plotly_chart(px.bar(grouped,x='stop_id',y='boardings',title='Boardings by Stop'),use_container_width=True)
    st.dataframe(grouped)

st.caption('Verify the data-quality summary before drawing operational conclusions. Filtered KPI and charts use the same selection.')
