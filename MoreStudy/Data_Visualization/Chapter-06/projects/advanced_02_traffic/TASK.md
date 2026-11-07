# Advanced Project — Urban Traffic Time Series Audit & Reporting

## 문제 상황

도로 구간의 시간대별 차량 통과 기록에서 시간대·누락·관측 완전성을 확인하고 자동 보고서를 생성합니다.

입력 데이터: `data/traffic_hourly.csv, data/traffic_corridors.json` (모두 교육용 가상 기록)

## 요구사항

1. UTC 시각을 Asia/Seoul로 변환한 다음 KST 기준 일별 집계를 수행합니다.
2. 음수·중복·미등록 도로·시간 해석 오류를 검출하고 감사 기록을 저장합니다.
3. 24개 시각이 모두 관측된 날짜만 유효한 일별 총통과량으로 집계합니다.
4. 동적으로 선택된 도로 구간마다 시계열 그래프를 작성합니다.
5. 평일·주말 시간대별 평균과 도로×시간대 Heatmap을 생성합니다.
6. 구간별 관측 완전성, 누락 개수, 생성한 보고서 파일을 검사합니다.

## 완료 조건

- 원본 데이터를 변경하지 않고 `output/`에 결과를 저장합니다.
- 결과 그래프의 시간대와 단위를 명확히 표기합니다.
- 결측·미관측값을 실제 0으로 단정하지 않습니다.
- 테스트가 검증하는 항목 외에도 그래프의 축·범례·레이아웃을 직접 점검합니다.

<details>
<summary><strong>힌트 1 — 데이터 구조</strong></summary>

시계열 인덱스 정렬, 예상 날짜 생성, 관측 단위부터 확인합니다.

</details>

<details>
<summary><strong>힌트 2 — 계산과 그림</strong></summary>

`reindex()`, `resample()`, `rolling()` 중 자료의 관측 단위에 맞는 연산을 선택합니다.

</details>
