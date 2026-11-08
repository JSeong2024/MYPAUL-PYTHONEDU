# R-01 — 성능 측정과 재현성 검증

[← Problems](../problem.md) · [← Summary 목차](../README.md)

`R-01.py`에는 실습용 합성 데이터 100,000건을 이용해 시설 기준 정보 조회 연산을 비교하는 코드가 포함되어 있습니다.

- 선형 검색과 Dictionary 조회에서 같은 시설의 수용 인원 배열이 생성되는지 비교합니다.
- `time.perf_counter()`로 처리 시간을, `tracemalloc`로 Python 메모리 할당의 최대값을 기록합니다.
- 모델 학습, CSV 파일 기록, 운영 평가 전체를 측정한 수치는 아닙니다.
- 실험 환경과 부하에 따라 측정 결과는 달라집니다. 성능 보고서에 적힌 시간을 재현성 판정용 고정값으로 비교하지 않습니다.

**재현성 검사 대상:** `clean_history.csv`, `rejected_rows.csv`, `split_report.json`, `model_report.json`, `test_predictions.csv`, `operational_predictions.csv`, `inspection_queue.csv`, `cluster_profiles.csv`, `final_report.md`의 내용과 순서입니다.

처리량을 늘리는 실험에서는 모든 검증 조건을 유지하고, 변경 전후의 예측·거부 결과가 정확히 같아야 합니다. 실제 실행에서 발생하는 시간·메모리 변동은 별도 측정 기록으로 보관합니다.
