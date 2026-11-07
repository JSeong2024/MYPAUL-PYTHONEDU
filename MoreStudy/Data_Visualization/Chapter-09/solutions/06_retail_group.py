from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

good,daily=retail_summary()

totals=good.groupby("store_id")["revenue_krw"].sum()
print(totals)
