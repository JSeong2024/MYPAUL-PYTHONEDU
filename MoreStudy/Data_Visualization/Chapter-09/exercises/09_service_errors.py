from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,transit_summary

good,summary=latency_summary()

# 과제: 전체 요청 중 오류 응답 비율을 `error_rate`에 저장
# TODO: 아래에 필요한 코드를 완성하세요.

# 실행 전에 TODO를 완성하세요.
