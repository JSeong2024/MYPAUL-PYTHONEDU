# Mini Project 02 — Service Latency Report

## 문제 상황

15분마다 측정한 응답 지연시간과 오류율을 두 개의 Axes로 표시하고, 공통 시간 범위를 탐색. 대상 데이터는 `data/`의 교육용 가상 기록이며, 값과 결측 규칙은 `DATA_DICTIONARY.md`를 따릅니다.

## 요구사항

1. 입력 열·날짜·단위·중복·값의 범위를 검사합니다.
2. 적절한 그래프 유형을 선택하고 Hover에 원본 단위를 표기합니다.
3. 범례 및 필요한 필터/범위 선택을 구현합니다.
4. 관측 누락과 실제 0을 혼동하지 않습니다.
5. 오프라인에서 열리는 HTML과 숫자 요약 JSON을 생성합니다.
6. 원본 CSV는 변경하지 않고 `output/` 아래에 결과를 기록합니다.

## 시작 파일 및 검증

- 시작 코드: `starter.py`
- 모범 구현: `../../solutions/mini_02_service/` (학습을 시도한 뒤 확인)
- `python -m unittest discover -s tests -v`로 공통 검증을 실행할 수 있습니다.

<details>
<summary><strong>Hint 01 — 출발점</strong></summary>

먼저 한 행의 관측 단위와 집계 기준을 확인하고, 한 개의 Figure만 완성해 봅니다.

</details>

<details>
<summary><strong>Hint 02 — Plotly 구성</strong></summary>

`px`로 빠르게 시작하되 여러 패널이나 세밀한 인터랙션은 `go`/`make_subplots()`를 고려합니다.

</details>

<details>
<summary><strong>Hint 03 — 파일 저장</strong></summary>

`fig.write_html(..., include_plotlyjs="directory")`는 같은 폴더에 JavaScript 번들을 함께 저장합니다. 둘 다 보존해야 오프라인에서 실행됩니다.

</details>
