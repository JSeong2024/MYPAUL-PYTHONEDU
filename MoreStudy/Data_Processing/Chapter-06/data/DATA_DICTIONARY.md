# Data Dictionary — Chapter 06

`raw_orders.csv`는 **교육용 가상 주문 데이터**입니다. 실제 개인·거래 정보가 아닙니다.

| Column | 자료형(원본) | 의미 | 처리 규칙 |
|---|---|---|---|
| `order_id` | 문자열 | 고유 주문 ID | `ORD-` + 3자리 숫자, 중복 불가 |
| `order_date` | 문자열 | 주문 일자 | `YYYY-MM-DD`, 2026년 10월 범위 |
| `customer_id` | 문자열 | 가상 고객 코드 | `C` + 3자리 숫자 |
| `region` | 문자열 | 주문 지역 | Seoul, Busan, Gwangju, Incheon |
| `category` | 문자열 | 상품군 | Food, Electronics, Stationery |
| `quantity` | 문자열 | 주문 수량 | 1~500 사이의 정수 |
| `unit_price` | 문자열 | 개당 가격(원) | 1~10,000,000 사이의 정수 |
| `status` | 문자열 | 주문 상태 | completed, pending, cancelled, refunded |

## 품질 규칙

- `raw_orders.csv`는 `dtype="string"`, `keep_default_na=False`로 읽어 원본 표기와 빈 문자열을 보존합니다.
- 공백을 제거한 뒤 비어 있는 필드는 결측으로 판단합니다.
- 중복 `order_id`의 **두 번째 이후 행**은 제외합니다. 이 프로젝트는 첫 기록을 우선하는 정책을 사용합니다. 실제 시스템에서는 충돌 유형을 추가 검토해야 합니다.
- 필수 필드·날짜·분류·수량·가격 검증에 실패한 레코드는 `rejected_orders.csv`로 분리합니다.
- 단가가 500,000원을 초과하는 행은 유효성 오류가 아니라 `review_orders.csv`로 분리합니다. 검토 승인 전 매출 집계에 넣지 않습니다.
- 완료 주문(`completed`)만 매출 집계에 포함합니다. 보류·취소·환불은 제외합니다.
- 원본 CSV와 품질 정책 JSON은 수정하지 않으며 결과는 `output/`에 저장합니다.

## 결과 파일

- `cleaned_orders.csv`: 자동 검증에 통과한 레코드(검토 대상 제외)
- `rejected_orders.csv`: 필수 검증에 실패한 레코드 및 사유
- `review_orders.csv`: 단가 검토 대상 레코드 및 사유
- `audit_log.csv`: 원본 각 행의 판정·사유
- `revenue_by_region.csv`: 완료 주문 지역별 집계
- `quality_report.json`: 원본/정제/제외/검토 건수 및 총매출
