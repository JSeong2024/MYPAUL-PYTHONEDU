# Data Dictionary

모든 데이터는 난수 시드를 고정하여 생성한 **교육용 가상 데이터**입니다. 기관의 공식 관측·측정 결과가 아닙니다. 단위는 파일에 기록한 정의를 따릅니다.

| 파일 | 시간 해석·관측 단위 | 주요 필드 | 의도된 조건 |
|---|---|---|---|
| `sales_daily.csv` | `date`: KST 일자, 매장 × 일자 | `store_id`, `revenue_krw` | 일부 날짜 기록 누락, 실제 매출 0원 존재 |
| `weather_hourly.csv` | `timestamp_local`: KST 현지 시각, 관측소 × 시각(1시간) | `temperature_c`, `precipitation_mm` | 관측 누락, 강수량 0mm 존재 |
| `server_metrics.csv` | `timestamp_utc`: UTC ISO 8601, 5분 | `cpu_pct`, `latency_ms` | 관측 누락과 일시적 성능 변화 |
| `air_quality_hourly.csv` | `timestamp_local`: KST 현지 시각, 관측소 × 시각(1시간) | `pm25_ug_m3` | 누락·중복·음수·문자열·미등록 ID |
| `traffic_hourly.csv` | `timestamp_utc`: UTC ISO 8601, 도로 구간 × 시각(1시간) | `vehicle_count` | 누락·중복·음수·잘못된 날짜·미등록 ID |

`air_stations.json`, `traffic_corridors.json`: 센서·도로 구간 기준정보. `timestamp_local`은 KST를 가정하며 시간대가 없는 문자열 자체만으로 KST가 자동 지정되지는 않습니다.

- `temperature_c`: 측정 시각의 기온(°C), 연속값. 시간별 평균과 일별 평균 가능.
- `precipitation_mm`: 해당 1시간 구간 강수량(mm), 겹치지 않는 구간의 합계 가능.
- `revenue_krw`: 해당 하루의 매출액(원), 일·주·월 합계 가능.
- `vehicle_count`: 해당 1시간 구간의 통과 차량 대수(대), 시간대별 합계 가능. 차량 밀도나 도로 점유율과는 다름.
- `pm25_ug_m3`: 해당 시각의 PM2.5 농도(µg/m³), 관측 평균 가능. 교육용 임계값은 공적 기준을 나타내지 않음.
- `cpu_pct`: 샘플 시점의 CPU 사용률(%). 합계 대신 평균·최댓값 등을 사용.
- `latency_ms`: 샘플 시점의 지연시간(ms). 표본 단위와 Percentile 계산 방식을 기록.

**결측값과 0 구분:** CSV에서 해당 시각의 행이 없다면 관측값을 알 수 없습니다. 측정값이 `0`인 행은 유효한 측정 결과일 수 있습니다. 파일을 생성하거나 가공하면서 누락 행을 자동으로 0으로 바꾸지 않습니다.
