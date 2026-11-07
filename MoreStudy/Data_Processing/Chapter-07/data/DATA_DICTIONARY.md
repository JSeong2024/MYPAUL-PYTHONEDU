# Data Dictionary — Store Sales Transformation

모든 데이터는 교육용 가상 데이터이며 개인 정보와 실제 거래 내역을 포함하지 않습니다. 금액 단위는 원(KRW)이고 부가세 및 반품은 고려하지 않습니다.

## order_lines.csv

| Column | Type | Meaning | Rule |
|---|---|---|---|
| `line_id` | string | 주문 행의 고유 식별자 | 중복 불가 |
| `order_id` | string | 주문 식별자 | 같은 주문에 복수 행 가능 |
| `order_date` | YYYY-MM-DD | 주문 기준 날짜 | 서울 시간 기준의 날짜만 저장(시간 정보 없음) |
| `store_id` | string | 매장 식별자 | `stores.csv` 참조 |
| `product_id` | string | 상품 식별자 | `products.csv` 참조 |
| `quantity` | int | 구매 수량 | 1 이상 |
| `unit_price_won` | int | 실제 적용된 행 단가(원) | 0 이상, 상품 목록의 기준가와 구분 |
| `discount_pct` | int | 정수 할인율(%) | 0 ~ 100 |

## products.csv

- `product_id`: 유일한 상품 식별자(Primary Key)
- `product_name`: 표시용 상품명
- `category`: 상품 분류
- `catalog_price_won`: 목록상 기준 단가. 주문의 실제 가격 계산에는 사용하지 않음

## stores.csv

- `store_id`: 유일한 매장 식별자(Primary Key)
- `store_name`: 표시용 매장명
- `region`: 지역명

## 금액 정책

`net_sales_won = quantity × unit_price_won × (100 − discount_pct) / 100`

금액이 원 단위 정수로 정확히 나누어떨어지는 데이터를 사용합니다. 소수 원 단위가 발생하는 입력은 **반올림을 임의로 적용하지 않고 오류**로 처리합니다. 실제 결제 시스템에서는 할인·세금·반올림 정책을 명시해야 합니다.

- 수량과 단가는 0 이상인 정수 범위를 먼저 검증합니다.
- 날짜는 자료에 기록된 `YYYY-MM-DD` 날짜 자체로 집계합니다. 시간대 변환을 수행하지 않습니다.
- 취소·환불 기록은 이 데이터셋에 포함하지 않습니다.
- **거래가 전혀 없는 날짜의 매출=0원**이라는 가정은 이 교육용 예제에서만 적용합니다. 수집이 누락된 날이라면 0으로 채우면 안 됩니다.
- 월별 집계는 `2026-01`, `2026-02` 같은 달력 월을 기준으로 합니다.
