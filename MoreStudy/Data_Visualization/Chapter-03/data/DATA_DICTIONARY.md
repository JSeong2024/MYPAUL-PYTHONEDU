# Data Dictionary — Chapter 03

모든 CSV 수치는 **교육용 가상 데이터**입니다. `subway_stations.csv`에는 실제 지하철역 이름이 사용되지만 승하차 인원은 실제 통계가 아닙니다. 어떤 기관의 공식 발표값도 나타내지 않습니다.

| File | Grain(한 행의 단위) | 주요 열 | 구분 |
|---|---|---|---|
| `weather_daily.csv` | 지역 × 날짜 | `date`, `region`, `temperature_c`, `precipitation_mm` | Mini 01 |
| `store_sales.csv` | 매장 × 분류 × 날짜 | `date`, `store`, `category`, `orders`, `revenue_krw` | Mini 02 |
| `server_metrics.csv` | 서비스 × 시간 | `timestamp`, `service`, `cpu_pct`, `memory_pct`, `response_ms` | Mini 03 |
| `weather_stations.csv` | 관측소 × 날짜 | `date`, `site_id`, `site_name`, `temperature_c`, `precipitation_mm` | Advanced 01 |
| `subway_stations.csv` | 역사 1개 | `station_id`, `station_name`, `line` | Advanced 02 |
| `subway_ridership.csv` | 역사 × 날짜 × 시간대 | `date`, `station_id`, `hour`, `boardings`, `alightings` | Advanced 02 |

### 파일별 조건과 주의

- `weather_daily.csv`: 14일 × 3지역 중 1행 누락, 온도값 1칸 결측. 원본 파일을 수정하지 않습니다.
- `store_sales.csv`: 28일 × 3개 매장 × 4개 분류 = **336행**. `revenue_krw`는 일별 매출액(원)이고 가상 데이터입니다.
- `server_metrics.csv`: 72시간 × 3서비스 = 216개 예정 슬롯, 3개 슬롯 부재, 응답시간 1개 결측. CPU·메모리는 백분율(%), 응답시간은 ms입니다. 임계값을 넘었다고 곧바로 장애로 판정하지 않습니다.
- `weather_stations.csv`: 30일 × 5개 관측소 = 150개 예정 슬롯, **5개 행 누락과 온도값 1개 결측**. 기온 0°C는 결측이 아닙니다.
- `subway_ridership.csv`: 2026-10-01~2026-10-28 × 8개 역사 × 매일 05~23시 = **4,256개 예정 슬롯**. 7개 슬롯 부재, 중복 행 2개, 유효하지 않은 승하차 숫자 3개가 포함됩니다. 결측 관측은 승하차 인원 0명과 다릅니다. 역별 승하차 통계만으로 열차 내 혼잡도를 결론 내릴 수 없습니다.

**공통 원칙:** 비교 그래프는 단위와 기간을 명확히 표기하고, 관측이 누락된 곳은 임의의 0으로 대체하지 않습니다. 실습 코드 출력은 `output/`으로 저장합니다.
