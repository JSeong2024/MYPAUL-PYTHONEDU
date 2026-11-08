# Chapter 04 — Data

Chapter 04의 CSV 파일 네 개는 `scripts/make_datasets.py`에서 생성한 **실습용 합성 데이터(Synthetic Data)** 입니다. 실제 시설의 고장 기록, 배송 이력, 측정 장비와 관련이 없습니다. 동일한 NumPy 시드로 생성하므로 파일을 재생성해도 결과가 같습니다.

| 파일 | Sample 수 | Feature | Target |
|---|---:|---|---|
| [`incident_alerts.csv`](./incident_alerts.csv) | 720 | `temperature_c`, `vibration_mm_s`, `current_a`, `operation_hours` | `flagged`(0: 일반, 1: 드문 사건) |
| [`delivery_times.csv`](./delivery_times.csv) | 560 | `distance_km`, `stop_count`, `traffic_index` | `actual_minutes`(분) |
| [`curve_measurements.csv`](./curve_measurements.csv) | 80 | `input_x` | `target_y` |
| [`device_cycles.csv`](./device_cycles.csv) | 600 | `fingerprint_signal`, `temperature_c` | `maintenance_flag`(0/1) |

## 사용 시 유의사항

- `alert_id`, `delivery_id`, `sample_id`, `device_id`는 기록을 구분하는 식별자이며, 일반적인 학습 Feature가 아닙니다.
- `flagged`, `maintenance_flag`는 Classification의 Label입니다. 두 값 모두 실습을 위해 생성한 값으로, 실제 고장 진단 기준이 아닙니다.
- `actual_minutes`는 Regression의 Target이며, `target_y`는 비선형 관계에 잡음을 추가한 수치입니다.
- `device_cycles.csv`에는 **하나의 장비가 6번 측정된 기록** 이 있습니다. `fingerprint_signal`은 장비별로 고정된 식별 신호로, 일반적인 예측 Feature로 사용할 가치가 없습니다. Advanced 02는 이 신호를 의도적으로 사용하여 잘못된 데이터 분할이 성능 평가를 어떻게 왜곡하는지 확인합니다.
- `device_id`가 같은 행들은 독립적인 Sample이 아닙니다. **새 장비에서의 성능** 을 알고 싶다면 장비 단위로 학습·평가를 분리해야 합니다.
- 같은 데이터라도 `random_state`, 분할 방식, 모델 설정이 달라지면 평가 결과가 달라질 수 있습니다.

## CSV 재생성

`Chapter-04/`에서 실행합니다.

```bash
python scripts/make_datasets.py
```

이 명령은 위 CSV 네 파일을 다시 생성합니다. 실습 중 데이터를 직접 수정했다면 실행 전에 백업하세요.

[← Chapter 04](../README.md) · [Contents](../README.md#contents)
