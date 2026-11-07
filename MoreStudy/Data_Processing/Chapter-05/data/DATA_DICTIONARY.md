# Chapter 05 — Dataset Dictionary

본 자료의 데이터는 **학습용 가상 데이터**입니다. 모든 파일은 저장소에 포함되어 있으며 인터넷 연결이 필요하지 않습니다.

## `orders.csv`

| Column | Type | Description |
|---|---|---|
| `order_id` | string | 주문의 고유 식별자 |
| `order_date` | ISO date text | 주문일 (`YYYY-MM-DD`) |
| `region_code` | string | 지역 식별 코드. `01`처럼 선행 0 보존 |
| `product_id` | string | 상품의 고유 식별자 |
| `quantity` | integer | 주문 수량, 1 이상 |
| `unit_price` | integer | 원화 단가, 0 이상 |
| `status` | string | `completed` 또는 `canceled` |

- 12개 주문 중 완료 10개, 취소 2개
- 완료 주문 합계 매출: **79,200원**
- 취소된 주문은 매출 집계에서 제외합니다.

## `products.json`

`schema_version=1`, `products` 목록 아래 상품 4개를 포함합니다. 각 항목은 `product_id`, `name`, `category`로 구성됩니다.

## `regions.xlsx`

- `Regions`: `region_code`, `region_name`, `zone`
- `Targets`: `region_code`, `target_revenue`
- 지역 코드의 선행 0을 유지하도록 문자열 자료형으로 읽습니다.
- `target_revenue`는 학습용 목표값이며 실제 통계 자료가 아닙니다.

## `readings.jsonl`

한 행에 JSON 객체 하나를 저장하는 JSON Lines 형식입니다. 센서 이름과 섭씨 온도 값이 포함됩니다.

## `api_response.json`

실제 서버 대신 사용하는 오프라인 API 응답 예시입니다. `source`, `data` 필드를 갖는 JSON 객체입니다.

## `notes.txt`

UTF-8 텍스트 파일이며, 파일 인코딩·줄바꿈·문자열 읽기 예제에 사용됩니다.

## 주의

데이터가 속한 단위, 인코딩, 필수 필드 및 변환 규칙은 파일 확장자만으로 자동 확정되지 않습니다. 스키마를 확인하고 읽기 옵션을 지정해야 합니다.
