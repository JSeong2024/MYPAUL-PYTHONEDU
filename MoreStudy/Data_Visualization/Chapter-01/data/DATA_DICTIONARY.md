# Data Dictionary — City Park Visits

`park_visits.csv`는 **교육용 가상 데이터**입니다. 실제 관측·출입 기록이 아닙니다.

| Field | Type | Meaning | Unit | Constraint |
|---|---|---|---|---|
| `date` | string (`YYYY-MM-DD`) | 관측 날짜(현지 날짜) | day | 중복·누락 없음 |
| `temperature_c` | float | 해당 날짜의 대표 기온(가상) | °C | 유한한 숫자, -30~45°C |
| `rainfall_mm` | float | 하루 누적 강수량(가상) | mm/day | 0 이상, 유한한 숫자 |
| `visitors` | integer | 해당 날짜 공원 방문 인원(가상) | 명/day | 0 이상의 정수 |

- 한 행의 단위(Grain)는 **하루**입니다. `date`는 고유해야 합니다.
- 강수량 `0.0`은 측정된 무강수 상태입니다. 결측값과 구분합니다.
- `temperature_c`는 실제 관측 원칙에 따른 일평균이 아니며 예제용 임의 수치입니다.
- 주말·공휴일·기상 변화 등의 조건이 통제되지 않았으므로 상관관계를 인과관계로 해석하지 않습니다.
- 이후 Chapter에서 추가로 수집할 실제 데이터는 출처, 이용 조건, 시각, 측정 단위 등을 별도로 검증해야 합니다.
