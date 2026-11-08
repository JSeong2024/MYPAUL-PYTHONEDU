# Chapter 02 — Data

모든 CSV는 Chapter 02 실습용 합성 데이터(Synthetic Data)입니다. 실제 배송 기록, 장비 진단 결과 또는 전력 사용 기록이 아닙니다. 난수 시드와 생성 규칙은 [`make_datasets.py`](../scripts/make_datasets.py)에 있습니다.

| 파일 | 행 수 | 입력 Feature | Target |
|---|---:|---|---|
| [`delivery_times.csv`](./delivery_times.csv) | 180 | `distance_km`(거리, km), `stops`(경유지 수) | `duration_min`(소요 시간, 분) |
| [`sensor_signals.csv`](./sensor_signals.csv) | 240 | `vibration_mm_s`(진동, mm/s), `ambient_lux`(조도, lx) | `fault_label`(0: 정상, 1: 이상) |
| [`energy_usage.csv`](./energy_usage.csv) | 320 | `temperature_c`(°C), `floor_area_m2`(㎡), `occupancy`(인원) | `energy_kwh`(kWh) |

`order_id`, `sample_id`, `record_id`는 행을 구분하는 식별자이며 Feature로 사용하지 않습니다.

`energy_usage.csv`의 `meter_finalized_kwh`는 **측정 종료 후에만 확정되는 값** 입니다. 예측 시점에 사용할 수 없으므로 정상적인 예측 모델의 Feature가 될 수 없습니다. Advanced Project 02에서 Data Leakage를 확인하기 위해 의도적으로 포함했습니다.

**재생성**

```bash
python scripts/make_datasets.py
```

CSV는 생성된 숫자를 반올림해 저장합니다. 계산에는 CSV에 기록된 값을 사용하세요.

[← Chapter 02](../README.md) · [Contents](../README.md#contents)
