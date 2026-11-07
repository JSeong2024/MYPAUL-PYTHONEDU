# Data Dictionary

모든 데이터는 교육용으로 생성한 **가상 데이터**입니다. 기업·기관의 실제 통계가 아닙니다.

| 파일 | 관측 단위 | 중요 열 | 주의점 |
|---|---|---|---|
| `shipments.csv` | 배송 건당 1행 | `carrier`, `zone`, `promised_days`, `actual_days`, `status` | `cancelled` 및 실제 소요일 누락 건은 정시배송 비율 분모에서 제외 |
| `support_tickets.csv` | 문의 건당 1행 | `team`, `priority`, `first_response_min`, `resolved` | 응답시간은 오른쪽으로 긴 꼬리 분포, 누락은 0분이 아님 |
| `inspections.csv` | 검사 건당 1행(원본엔 중복 포함) | `inspection_id`, `plant`, `line`, `shift`, `thickness_mm`, `is_defective` | `inspection_id` 중복 4건, 두께 결측 및 비현실적인 값 있음 |
| `simpson_delivery.csv` | 가상 배송 건당 1행 | `carrier`, `zone`, `on_time` | 집계 수준이 달라지면 방향이 뒤집히는 교육용 사례 |

## 정의

- **정시 배송:** `status == delivered`이며 `actual_days <= promised_days`인 건. 소요일이 없으면 정시 여부는 결측으로 처리합니다.
- **첫 응답시간:** 문의 접수 후 최초 응답까지의 분. 해결 시간과 다릅니다.
- **불량률:** 검사 건 중 `is_defective == 1`의 비율. 검사 표본만의 비율이며 전체 생산량의 불량률을 보장하지 않습니다.
- **두께 측정 허용 범위(학습 가정):** 8mm 이상 12mm 이하. 실제 제품의 규격이 아닙니다.
- **범주:** `plant`와 `line`은 소속 관계가 일치해야 합니다.
- **데이터 출처:** NumPy의 난수 생성기(seed 20261107)로 가상 생성.

## 해석 유의사항

- 실제 0, 결측, 미측정, 취소는 구분합니다.
- 비율과 평균은 관측된 데이터 집합에 대해서만 해석합니다.
- 상관관계 및 집단 차이만으로 원인이나 정책 효과를 단정하지 않습니다.
- 데이터 생성에는 실제 업체·기관의 기록이 사용되지 않았습니다.
