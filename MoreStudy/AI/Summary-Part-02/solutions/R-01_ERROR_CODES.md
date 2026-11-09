# R-01 — 오류 및 차단 기준

[← Problems](../problem.md) · [Summary 목차](../README.md)

| 오류 코드 | 발생 조건 | 처리 |
|---|---|---|
| `UNKNOWN_SITE` | 시설 기준 목록에 없는 Site | 해당 행 거부 |
| `INVALID_DATE` | 날짜 형식 오류 | 해당 행 거부 |
| `INVALID_VALUE` | 필수 수치 누락·비유한 값·범위 위반 | 해당 행 거부 |
| `INVALID_TARGET` | 과거 기록의 Label 또는 Target 값 오류 | 해당 행 거부 |
| `DUPLICATE_RECORD` | 앞선 유효 기록과 동일 `(site_id,date)` | 이후 행 거부 |
| `SHIFT_ALERT` | 유효 Incoming 30건 이상이고 학습 범위 밖 기록 비율이 20% 초과 | 점수 기록 가능, 자동 점검 확정 차단 |
| `NO_ROLLBACK_TARGET` | 이전 정상 배포 기록 없음 | 기존 활성 버전 유지 |

오류 판정은 위 표의 처음 다섯 행 순서대로 수행합니다. **무효 행은 중복 검사 키를 점유하지 않습니다.**

모델·Checkpoint 파일은 신뢰할 수 있는 프로젝트 산출물만 읽으며, 모델 상태나 기준 결과가 유효하지 않으면 활성 버전을 변경해서는 안 됩니다.
