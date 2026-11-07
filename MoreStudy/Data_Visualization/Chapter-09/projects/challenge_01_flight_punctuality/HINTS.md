# 단계별 힌트

<details>
<summary><strong>Hint 01 — 관측 단위</strong></summary>

먼저 한 행이 어떤 단위를 나타내는지 정하고, 집계 기준과 유일 키를 분리하세요.

</details>

<details>
<summary><strong>Hint 02 — 유효성 검사</strong></summary>

관측소/역/지역의 참조 ID, 시간 변환 실패, 범위 위반을 각각 다른 사유로 기록하세요.

</details>

<details>
<summary><strong>Hint 03 — 검증과 시각화 분리</strong></summary>

순수 함수가 DataFrame을 반환하도록 구성하면 화면 코드 없이도 수치 계산을 테스트할 수 있습니다.

</details>

<details>
<summary><strong>Hint 04 — 완료 기준</strong></summary>

원본 행 수 = 유효 행 수 + 제외 행 수가 성립하는지 확인하고, 누락된 *슬롯* 수와 제외된 *행* 수를 구분하세요.

</details>
