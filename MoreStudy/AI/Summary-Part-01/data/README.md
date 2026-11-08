# 실습용 합성 데이터

[← Summary 목차](../README.md) · [Problems](../problem.md)

`data/문제번호/`에는 프로젝트형 문제를 실행하는 데 필요한 CSV 파일이 들어 있습니다. 개인 정보나 실제 운영 기록은 포함되어 있지 않습니다.

| 문제 | 입력 데이터 | 구성 |
|---|---|---|
| A-01 | `validation_scores.csv`, `test_scores.csv` | 임계값 선택과 독립 평가 |
| A-02 | `daily_water.csv` | 날짜별 수도 사용량 예측 |
| A-03 | `space_usage.csv` | 방문 패턴과 오류 행 포함 |
| A-04 | 별도 CSV 없음 | 코드에서 `make_classification()` 실행 |
| P-01 | `historical_claims.csv`, `incoming_claims.csv` | 제품별 반복 수리 접수와 운영 요청 |
| P-02 | `weekly_waste.csv` | 구역별 주간 수거량 |
| P-03 | `workspace_usage.csv` | 공간·주차별 예약 패턴 |
| C-01 | `equipment_history.csv` | 설비별 반복 측정과 사후 기록 |
| C-02 | `history_v1.csv`, `incoming_v2.csv` | 온도 단위 변경과 무효 입력 |
| R-01 | `facilities.csv`, `daily_operations.csv`, `incoming_operations.csv` | 시설 참조·과거 관측·운영 입력 |

Basic 5문항은 표준 입력을 이용하므로 별도 CSV 파일이 없습니다.

동일한 시드로 데이터를 재생성하려면 Chapter 폴더에서 다음 명령을 실행합니다.

```bash
python tests/generate_data.py --output data
```

CSV를 수정해 다른 오류 상황을 만들어 볼 수 있습니다. 기존 데이터를 덮어쓰지 않으려면 먼저 별도 작업 폴더로 복사하세요. 데이터는 문제의 기술 명세를 검증하기 위한 실습용이며, 실제 현장에서 발생할 법한 모든 입력 분포를 대표하지 않습니다.
