# Data Dictionary

모든 데이터는 교육용 가상 데이터입니다. 실제 매출·방문·서비스·자전거 이용 통계가 아닙니다.

## `retail_orders.csv`
- `order_id`: 주문 상품 행 ID. 각 행은 하나의 주문 항목으로 가정합니다.
- `date`: 거래 일자(YYYY-MM-DD).
- `branch`: 매장 이름.
- `channel`: In-store / Online / Pickup.
- `category`: 상품 분류.
- `units`: 판매 수량(개).
- `unit_price_krw`: 단가(원).
- `status`: Completed / Returned. Returned는 `revenue_krw`에서 0으로 처리됩니다(환불 순효과 계산이 아님).
- `revenue_krw`: Completed 주문의 금액. 해당 데이터셋은 순매출·환불 정산을 나타내지 않습니다.

## `service_requests.csv`
- `request_id`: 개별 요청 ID.
- `service`: Auth / Catalog / Checkout / Search.
- `priority`: Standard / Urgent.
- `hour`: 요청 시각의 시간(0–23).
- `response_ms`: 응답 시간(ms). 긴 오른쪽 꼬리를 가진 분포를 시뮬레이션했습니다.
- `failed`: 요청 실패 여부(0/1).
- `day`: 요청 날짜.

## `library_visits.csv`
- `date`, `branch`: 분관·날짜별 관측 단위(1일 1행).
- `visitors`: 그날 실제 집계 방문자 수(명).
- `new_members`: 신규 등록자 수(명).
- `open_hours`: 개관 시간(시간).
- East 10월 11일, South 10월 22일은 행 자체를 누락했습니다. 이 날짜는 방문자 0명이 아닙니다.

## Advanced — Public bicycle demand
- `bike_stations.csv`: 역사 명칭이 아닌 교육용 대여소(ID, 이름, 구역).
- `bike_reporting.csv`: 날짜 × 대여소 × 시간대별 집계 가능 여부(`reporting`: 1/0).
- `bike_trips.csv`: 개별 이용 기록(`ride_id`, `date`, `station_id`, `time_band`, `duration_min`, `user_type`).
- 시각화 집계의 단위는 `date × station_id × time_band` 슬롯이며, `reporting=0`은 **자료 부재**입니다.
- `reporting=1`이며 이용 기록이 없는 슬롯은 **0건으로 판단 가능**합니다.
- `bike_trips.csv`에 고의적인 오류 4행과 중복 1행을 포함했습니다. 검증 규칙에 따라 제외합니다.
- 측정값, 역·대여소 표기, 장소 및 지역별 수치는 현실 통계가 아닙니다.
