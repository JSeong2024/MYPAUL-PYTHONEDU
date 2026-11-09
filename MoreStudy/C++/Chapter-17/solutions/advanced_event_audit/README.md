# Advanced Project — Event Audit

센서 장비의 증감 이벤트를 원본 순서대로 처리하고, 유효하지 않은 행을 별도 로그로 분리합니다.

## 규칙

- 입력 파일 `events.csv`는 헤더 없는 `event_id,device_id,ADD|REMOVE,amount` 구조입니다. 따옴표와 필드 안의 쉼표는 지원하지 않습니다.
- 모든 ID는 빈 문자열이 아니어야 합니다. 금액은 `1..1,000,000`의 정수입니다.
- 성공적으로 적용된 이벤트 ID만 중복 처리 대상으로 등록합니다. 이전에 거부한 동일 ID를 다시 사용하는 것은 허용됩니다.
- `REMOVE`는 현재 잔액을 초과할 수 없습니다. 거부된 이벤트는 어떤 잔액도 변경하지 않습니다.
- `balances.csv`는 장치 ID 오름차순이고, `rejected.csv`는 원본 행번호와 오류 코드의 입력 순서입니다.
- 결과 파일은 프로그램이 열어 직접 기록합니다. 파일 간 원자적 교체는 이 프로젝트 범위 밖입니다.
- 비정상 행의 오류 우선순위: 형식 → 금액 → 유형 → 중복 → 잔액 초과. 전체 입력 파일의 총 행 수와 금액 합계가 64비트 정수 범위를 넘지 않는 규모를 가정합니다.

```bash
cmake -S . -B build -DCMAKE_CXX_STANDARD=20
cmake --build build
ctest --test-dir build --output-on-failure
./build/audit_cli data/events.csv build/balances.csv build/rejected.csv
```

학생용 프로젝트는 `../../projects/advanced_event_audit/`에 있으며 처리 로직이 TODO입니다.
