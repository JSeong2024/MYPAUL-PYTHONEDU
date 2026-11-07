# Advanced 01 — 모범 구현 설명

이 프로젝트의 목적은 **Plotly 그래프만 그리는 것이 아니라 데이터의 신뢰도를 유지한 상태로 탐색 기능을 구현하는 것**입니다.

1. `validate_energy()`는 UTC 날짜 변환, 지역 ID, 음수·문자열, 중복 키를 검사합니다. 중복된 슬롯은 두 기록 모두 제외해 임의 선택을 방지합니다.
2. `make_expected_grid()`는 KST 지역별 예정 시간 슬롯을 모두 생성하고 기존 기록을 왼쪽 결합합니다. 결측은 `NaN`으로 유지합니다.
3. `make_figure()`는 두 패널에 각 지역의 Trace 2개를 추가합니다. 드롭다운 버튼 하나가 같은 지역의 두 Trace를 함께 표시합니다.
4. `rangeslider_visible=True`는 그래프의 X축 범위를 바꿉니다. 전체 원본을 제거하거나 서버에서 다시 계산하지 않습니다.
5. `summary.json`, `invalid_rows.csv`, `hourly_coverage.csv`는 그래프의 수치 검토와 감사에 사용합니다.

**주의:** `demand_kw`는 시점 전력 수요이고 에너지 소비량이 아닙니다. 1시간마다 측정했다는 이유로 kW를 합쳐 kWh라고 표기하지 않습니다. 시간별 시점값을 그대로 사용하고 평균·최댓값만 비교합니다.

다른 접근: Plotly Express로 그래프를 먼저 생성한 뒤 `go.Figure`에 Trace를 복사할 수 있습니다. 다만 드롭다운의 Trace visibility와 subplot axis 매핑을 명시적으로 관리하는 편이 데이터 선택을 검증하기 쉽습니다.
