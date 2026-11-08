# R-01 — 데이터 검증 오류 코드

[← Problems](../problem.md) · [← Summary 목차](../README.md)

| 오류 코드 | 의미 | 처리 |
|---|---|---|
| `UNKNOWN_FACILITY` | 기준 정보에 없는 `facility_id` | 해당 기록 거부 |
| `INVALID_NUMBER` | 날짜 형식 오류, 결측값, 수치 형식 또는 범위 오류 | 해당 기록 거부 |
| `INVALID_TARGET` | 과거 Classification 또는 Regression Target 형식·범위 위반 | 해당 기록 거부 |
| `DUPLICATE_RECORD` | 같은 시설·날짜의 유효한 기록이 이미 채택됨 | 나중에 들어온 유효 행 거부 |

`source_line`은 CSV 헤더가 첫 줄일 때의 실제 행 번호입니다. 무효 행은 시설·날짜 중복 검사에서 키를 선점하지 않습니다. 기준 정보인 `facilities.csv`의 중복 시설 ID 또는 필수 열 누락은 전체 실행 중단 사유입니다.

분석에 실패할 경우 `results/`의 이전 결과를 새 결과로 바꾸지 않습니다. 데이터와 실행 파일은 같은 작업 디렉터리에서 관리하며, 보고서의 값은 원본 데이터에 따라 달라집니다.
