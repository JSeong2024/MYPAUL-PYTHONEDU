from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

good,bad,daily=electricity_summary()

average_mw=good.groupby("region")["demand_mw"].mean()
print(average_mw)
