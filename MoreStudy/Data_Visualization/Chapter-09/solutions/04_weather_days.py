from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

good,bad,daily,slots=weather_summary()

complete_days=int(daily["readings"].eq(2).sum())
print(complete_days)
