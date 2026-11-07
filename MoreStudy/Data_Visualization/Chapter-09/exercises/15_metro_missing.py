from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

good,bad,daily,slots=metro_summary()

# 과제: 예정되었으나 유효 기록이 없는 슬롯 수를 `missing_slots`로 저장
# TODO: 아래에 필요한 코드를 완성하세요.

# 실행 전에 TODO를 완성하세요.
