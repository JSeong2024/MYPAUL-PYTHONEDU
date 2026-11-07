# Data Dictionary

모든 데이터는 교육용 가상 기록입니다. 실제 관측치·공식 통계가 아닙니다.

| File | Grain | 주요 필드 | 비고 |
|---|---|---|---|
| `weather_observations.csv` | 관측소·시각 | `temperature_c`, `precipitation_mm` | KST 가정, 하루 2회 |
| `stations.csv` | 관측소 | `station_id`, `region` | 참조 테이블 |
| `retail_orders.csv` | 주문상품 행 | `quantity`, `unit_price_krw` | 취소 제외 매출 |
| `service_latency.csv` | 요청 | `latency_ms`, `is_error` | 응답 지연의 중위수·P95 |
| `electricity_demand.csv` | 지역·UTC 시간 | `demand_mw` | MW는 전력, 단순 합계는 에너지 아님 |
| `metro_boardings.csv` | 역·KST 시간 | `boardings` | 예정 05–22시, 누락 관측 주의 |
| `metro_stations.csv` | 역 | `station_id`, `line` | 참조 테이블 |
| `flights.csv` | 공항·날짜·편 슬롯 | `delay_min`, `late_flag` | 가상 운항 기록 |
| `transit_stops.csv` | 정류장 | `stop_id`, `line`, `zone` | 참조 테이블 |
| `transit_operations.csv` | 정류장·KST 시간 | `boardings`, `delay_min` | 예정 06–22시 |
| `transit_incidents.csv` | 사고 | `incident_id`, `category`, `duration_min` | 원인 추론 불가 |

**결측**: 관측 레코드가 존재하지 않는 것은 0과 다릅니다. **중복 관측 슬롯**: 어떤 행이 올바른지 모르면 동일 슬롯의 양쪽 기록을 모두 검토 대상으로 분리합니다. **시간대**: 시각 문자열에 오프셋이 없다면 소스에서 명시한 시간대 규칙을 확인해야 합니다.
