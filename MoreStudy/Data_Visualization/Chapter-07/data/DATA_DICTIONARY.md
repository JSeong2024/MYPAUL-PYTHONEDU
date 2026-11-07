# Data Dictionary

모든 CSV는 **교육용 가상 데이터**입니다. 실제 상점, 서비스, 기관, 지역의 관측 결과가 아닙니다. 생성 과정에서 난수 시드를 고정했습니다.

| 파일 | 관측 단위 | 필드 | 주의점 |
|---|---|---|---|
| `retail_sales.csv` | 날짜 × 매장 × 상품 분류 | `date`, `store`, `category`, `units`, `unit_price_krw`, `revenue_krw` | 일부 행 누락; 실제 0건 판매와 구별 |
| `service_metrics.csv` | UTC 15분 × 서비스 | `timestamp_utc`, `service`, `p95_latency_ms`, `error_requests`, `total_requests` | p95는 각 15분 구간의 95백분위 지연시간; 구간별 p95의 단순 평균은 전체 요청의 p95가 아님 |
| `support_tickets.csv` | 문의 1건 | `ticket_id`, `created_local`, `team`, `priority`, `first_response_min`, `status` | 응답시간은 최초 응답까지 경과 분; 교육용 값 |
| `regional_energy_hourly.csv` | UTC 1시간 × 지역 | `timestamp_utc`, `region`, `demand_kw` | 시점 전력 수요(kW), 에너지 소비량(kWh)이 아님; 일부 결측 슬롯과 잘못된 입력 포함 |

- `regional_energy_hourly.csv`: 시각은 UTC이고, 일별 비교 시 `Asia/Seoul`로 변환해야 합니다.
- 예상 시간 슬롯은 2026-09-01 00:00 KST부터 2026-10-05 23:00 KST까지 각 지역별 1시간 단위입니다.
- `demand_kw`는 한 시각에 측정한 전력 수준입니다. 시간별 통계를 합쳐 사용량처럼 해석하면 안 됩니다. 1시간 간격의 평균 전력값으로 간주한다면 에너지량을 계산할 수 있지만 이 데이터는 시점값으로 정의합니다.
- API/브라우저 연결 없이 사용 가능한 로컬 데이터입니다.
