# Dataset Dictionary — Weather Observations

본 프로젝트의 데이터는 **교육용 가상 데이터**이며 실제 기상 관측 결과가 아닙니다.

## `weather_observations.csv`

| Column | Type | Meaning |
|---|---|---|
| `observation_id` | string | 측정 기록을 식별하는 고유 ID |
| `timestamp_local` | `YYYY-MM-DD HH:MM` | 한국 표준시(KST)로 기록한 현지 시각 (시간대 정보는 문자열에 포함하지 않음) |
| `station_id` | string | 관측소 식별자, `stations.json`과 결합 키 |
| `temperature_c` | float | 섭씨 기온(°C). 빈 값은 측정값 없음 |
| `humidity_pct` | float | 상대습도(%), 정상 범위 0~100 |
| `precipitation_mm` | float | 이전 관측 시점부터 해당 시점까지의 강수량(mm). 0은 실제 0mm 관측 |

**관측 계획:** 2026-10-01~2026-10-14, 관측소 3개, 매일 09:00 및 18:00의 총 84개 슬롯. `ST-02`의 10월 9일 관측 2건은 **파일에 아예 존재하지 않도록** 구성했습니다. 따라서 `0mm`와 관측 누락을 혼동하지 않아야 합니다.

파일 끝에는 실습을 위한 오류 기록 10행이 추가되어 있습니다. 일련번호가 맞더라도 ID 중복, 날짜 오류, 미등록 관측소, 자료형 오류 등은 별도 검증해야 합니다.

## `stations.json`

| Field | Meaning |
|---|---|
| `station_id` | 관측소 식별자 (유일) |
| `region` | 지역명 |
| `elevation_m` | 해발고도(m) |

## `cleaning_policy.json`

- 날짜 범위: 2026-10-01~2026-10-14, 양 끝 포함
- 허용 관측 시각: 09:00, 18:00 (KST)
- 기온: -30~45°C, 범위를 벗어나거나 비어 있으면 `review` 처리
- 습도: 0~100%, 범위를 벗어나면 `rejected` 처리
- 강수량: 0mm 이상, 음수이면 `rejected` 처리
- 수치형 값의 공백·문자열 오류: `review` 처리
- 중복 ID, 동일 관측소·시각 중복, 잘못된 날짜, 미등록 관측소, 식별자 누락: `rejected` 처리

`review`와 `rejected` 기록은 **집계에서 제외**하되 원본과 사유를 `issues.csv`에 남깁니다. 데이터가 없는 날을 자동으로 0으로 채우지 않습니다. 이 정책은 실제 기관의 관측값 검증 기준이 아닌 학습용 규칙입니다.

## 집계 정의

- `daily_station_summary.csv`: 관측소·날짜별 기온/습도 평균, 관측 구간 강수량 합계, 수집 건수
- `station_summary.csv`: 관측소별 유효 기록 건수, 기온 요약, 강수량 합계
- `monthly_region_summary.csv`: 관측값 기준 지역·월별 기온 평균, 강수량 합계, 유효 관측 수
- `coverage.csv`: **예상 관측 슬롯**과 실제 유효 기록 건수를 비교. 관측 0건은 `missing`, 1건은 `partial`, 2건은 `complete`
- `quality_report.json`: 상태별 건수와 오류 원인 및 전체 관측 커버리지

집계된 기온 평균은 해당 기간에 유효하게 관측된 값의 평균이며, 관측 공백을 메우거나 관측소의 장기적인 기후 특성을 추정하는 통계가 아닙니다.
