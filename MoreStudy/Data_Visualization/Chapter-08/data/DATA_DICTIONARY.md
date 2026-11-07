# Data Dictionary

모든 데이터는 **교육용 가상 데이터**입니다. 실제 매장·시설·기관의 운영 현황을 나타내지 않습니다.

| 파일 | 한 행의 의미 | 핵심 열 | 단위 및 주의사항 |
|---|---|---|---|
| `retail_daily.csv` | 날짜 × 매장 × 분류 | `date`, `store`, `category`, `quantity`, `revenue_krw` | 수량은 건, 매출은 KRW (합계 가능) |
| `service_hourly.csv` | UTC 1시간 × 서비스 | `timestamp_utc`, `service`, `requests`, `errors`, `p95_ms` | 요청·오류는 건수; p95는 ms, 단순 평균 집계 주의 |
| `tickets.csv` | 고객문의 1건 | `ticket_id`, `team`, `status`, `first_response_hours` | 응답시간은 시간; Open은 미해결 상태 |
| `metro_hourly_raw.csv` | KST 1시간 × 역사 | `timestamp_kst`, `station_id`, `boardings`, `avg_delay_min`, `trips_observed` | 승차 인원은 시간대별 합계, 지연은 그 시간대 측정 평균 |
| `stations.json` | 역 기준정보 1건 | `station_id`, `line`, `label` | 역사 ID는 유일해야 함 |
| `rail_policy.json` | 허용 날짜와 시간 간격 | `start_date`, `end_date`, `timezone` | 14일·7개 역사·시간당 1건 가정 |

### 중요한 구별

- `boardings = 0`은 **해당 슬롯을 관측했고 승차 인원이 0명**이라는 뜻입니다. 기록 자체가 없거나 검증에서 제외된 슬롯과 다릅니다.
- `avg_delay_min`은 시간대의 평균으로, 관측 횟수를 고려하지 않은 평균의 평균은 정확하지 않을 수 있습니다. 예제는 보고서에 단순 평균을 쓰되 이러한 한계를 표시합니다.
- `service_hourly.csv`의 `p95_ms`는 시간대별 p95입니다. 시간대 p95를 평균해도 전체 요청의 p95가 되는 것은 아닙니다.
- 날짜가 날짜 문자열인 데이터는 현지 날짜, UTC 표기가 있는 데이터는 UTC로 해석합니다.
- `metro_hourly_raw.csv`에는 누락·음수·중복·미등록 역사·잘못된 날짜가 의도적으로 포함됩니다. 집계 전에 검사해야 합니다.
