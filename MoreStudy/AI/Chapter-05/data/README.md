[← Chapter 05](../README.md) · [Mini Projects](../README.md#section-5-13) · [Advanced Projects](../README.md#section-5-14)

# 실습 데이터

이 폴더의 CSV는 모두 **실습용 합성 데이터**입니다. 실제 시설 운영이나 품질 관리에 사용하기 위한 자료가 아닙니다.

| 파일 | 행 수 | 생성 방식 | 용도 |
|---|---:|---|---|
| `sensor_readings.csv` | 20 | 시간별 변동과 특정 위치의 결측 표시 `-1` | Mini 01 |
| `calibration_pairs.csv` | 12 | 선형 신호와 작은 잡음 | Mini 02 |
| `facility_events.csv` | 48 | 온도·진동·시간과 이진 경보 규칙 | Advanced 01 |
| `facility_events_invalid.csv` | 3 | 온도 결측값을 포함한 의도적인 오류 입력 | Advanced 01 유효성 검사 |
| `gradient_audit.csv` | 13 | `tanh` 함수와 작은 잡음 | Advanced 02 |

## 주요 열

- `sensor_readings.csv`: `day`, `sensor_01`~`sensor_04`. 측정 실패는 `-1`이며 정상 측정은 0 이상입니다.
- `calibration_pairs.csv`: `input_signal`, `reference_value`. `reference_value`는 합성 보정 목표입니다.
- `facility_events.csv`: `event_id`, `zone`, `hour`, `temperature_c`, `vibration_mm_s`, `alert_label`. `event_id`와 `zone`은 메타데이터이고 Feature에는 포함하지 않습니다.
- `gradient_audit.csv`: `input_signal`, `target_value`. 두 값 모두 실수입니다.

## 재생성

저장소의 `Chapter-05/` 폴더에서 실행합니다.

```bash
python scripts/make_datasets.py
```

`random.Random(2026)`을 사용하며 외부 서버와 인터넷 연결이 필요하지 않습니다. 실행하면 CSV 5개를 덮어쓰므로, 실습 중 변경한 데이터를 보관해야 한다면 먼저 별도 이름으로 복사해 두세요.

---

[← Chapter 05](../README.md) · [Contents](../README.md#contents)
