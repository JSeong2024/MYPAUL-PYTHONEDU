# Mini Project — Server Metrics Monitoring

## 문제 상황

5분 간격의 CPU 사용률과 응답 지연을 분석하여 수집 공백과 일시적 급증을 시각화합니다.

입력 데이터: `data/server_metrics.csv` (모두 교육용 가상 기록)

## 요구사항

1. UTC 문자열을 timezone-aware timestamp로 변환합니다.
2. 5분 간격의 전체 슬롯을 복원하고 누락을 표시합니다.
3. CPU 기준선과 1시간 이동평균을 포함한 2행 그래프를 작성합니다.
4. 관측 수·누락 수·최댓값을 JSON으로 출력합니다.

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
