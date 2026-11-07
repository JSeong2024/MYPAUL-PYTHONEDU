from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

good,summary=latency_summary()

p95=good.groupby("service")["latency_ms"].quantile(.95)
print(p95)
