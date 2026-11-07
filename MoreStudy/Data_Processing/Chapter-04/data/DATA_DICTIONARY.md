# Dataset — `orders.csv`

교육용 가상 주문 데이터로, 실제 개인·기업·거래 정보를 포함하지 않습니다. 통화 단위는 원(KRW)이며 금액에는 세금·수수료·배송비를 반영하지 않습니다.

| Column | Type | Description | Example |
|---|---|---|---|
| `order_id` | String | 주문 고유 ID | `ORD001` |
| `order_date` | Date String (ISO 8601) | 주문 일자 | `2026-10-01` |
| `region` | String | 지역 | `서울`, `부산`, `인천` |
| `category` | String | 상품 분류 | `음료`, `문구`, `전자` |
| `product` | String | 상품명 | `커피` |
| `quantity` | Integer | 주문 수량, 1 이상 | `2` |
| `unit_price` | Integer (KRW) | 상품 단가, 0 이상 | `3500` |
| `status` | String | 주문 상태: `completed` / `canceled` | `completed` |

- 20개 주문, `completed` 17개, `canceled` 3개
- **매출액 정의:** `status == "completed"`인 주문의 `quantity * unit_price` 합계
- 모든 수치가 유효하도록 구성했습니다. 오류 데이터 복원·정제는 Chapter 06에서 다룹니다.
- 예제는 원본 CSV를 읽기만 하며, 저장 결과는 `output/`에 생성됩니다.
