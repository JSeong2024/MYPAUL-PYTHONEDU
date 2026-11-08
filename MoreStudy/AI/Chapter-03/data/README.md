# Chapter 03 — Data

Chapter 03의 CSV 네 개는 `scripts/make_datasets.py`로 생성한 **실습용 합성 데이터(Synthetic Data)** 입니다. 실제 고객, 시설, 근무자 또는 이동 경로의 통계가 아닙니다. 정수 시드를 고정하여 재생성할 때 같은 데이터가 나오도록 했습니다.

| 파일 | 행 수 | 입력 Feature | Target 또는 참고 정보 |
|---|---:|---|---|
| `service_tickets.csv` | 480 | `waiting_hours`, `failed_attempts`, `impacted_users` | `urgent` (0: 일반, 1: 긴급) |
| `station_patterns.csv` | 270 | `morning_trips`, `evening_trips`, `weekend_trips` | Target 없음 |
| `work_modes.csv` | 540 | `morning_activity`, `remote_activity`, `evening_activity` | `work_mode` (0, 1, 2) |
| `curved_paths.csv` | 464 | `x_position`, `y_position` | `reference_group` (0, 1, -1) |

- `ticket_id`, `station_id`, `record_id`, `point_id`는 행 식별자이며 모델 입력에서 제외합니다.
- `urgent`와 `work_mode`는 Supervised Learning의 Target입니다. KMeans나 DBSCAN에 전달하지 않습니다.
- `reference_group`은 군집화 결과의 **사후 평가에만** 사용합니다. `-1`은 데이터 생성 시 추가한 참고용 Noise를 표시합니다. DBSCAN이 부여하는 `-1`과 일치한다고 보장되지는 않습니다.
- `station_patterns.csv`는 Label을 제공하지 않습니다. 각 Cluster의 이름과 의미는 Cluster Profile을 계산한 뒤 해석합니다.

## 데이터 생성

`Chapter-03/`에서 실행합니다.

```bash
python scripts/make_datasets.py
```

이 명령은 네 CSV를 다시 생성하여 덮어씁니다. 개별 프로젝트는 CSV 생성에 사용된 숨은 수식이나 그룹 구성을 모른다고 가정하고 문제를 해결합니다.

[← Chapter 03](../README.md) · [Contents](../README.md#contents)
