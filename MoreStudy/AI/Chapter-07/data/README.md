[← Chapter 07](../README.md) · [Contents](../README.md#contents)

# 실습 데이터

세 CSV는 `scripts/make_datasets.py`로 생성한 **실습용 합성 데이터** 입니다. 실제 설비 기록이나 운영 보고 자료가 아닙니다. 인터넷 연결 없이 모든 예제와 프로젝트를 실행할 수 있습니다.

| 파일 | Sample 수 | 학습 과제 | 주요 Feature |
|---|---:|---|---|
| [`energy_demand.csv`](./energy_demand.csv) | 360 | Regression · Optimizer/Regularization/Resume | `hour`, `temperature_c`, `occupancy`, `is_weekend` |
| [`device_alerts.csv`](./device_alerts.csv) | 420 | Binary Classification · LR/Gradient | `vibration`, `temperature_c`, `load_factor`, `days_since_service` |
| [`fleet_events.csv`](./fleet_events.csv) | 768 | Professional · 신규 시설의 정비 위험 예측 | `equipment_type`, `vibration`, `temperature_c`, `utilization`, `days_since_service`, `prior_alerts` |

## 데이터 생성 및 해석

### Energy Demand

시간대·온도·이용량·주말 여부에 따른 비선형 수요 관계에 난수를 섞었습니다. `demand_kwh`는 정답 Target이며, `observation_id`는 행 추적용 ID입니다. 파일 순서는 생성 순서에 따른 시간 흐름으로 간주합니다. 실제 날짜나 특정 시설 운영 정책을 의미하지 않습니다.

Train은 앞의 240건, Validation은 다음 60건, Test는 마지막 60건으로 고정합니다. Feature와 Target Scaling의 평균·표준편차는 Train에 대해서만 계산합니다. 일반화를 확인하는 프로젝트에서 Train 구간의 네 번째 Sample마다 하나씩 선택하는 경우에도 Scaling 기준은 원래 Train 구간입니다.

### Device Alerts

`alert_label`은 0 또는 1이며, 입력 Feature의 가중합과 상호작용에 따라 사건 가능성이 달라지는 확률 분포에서 샘플링했습니다. 특정 입력이 정답을 완전히 결정하지 않기 때문에 100% Accuracy를 목표로 삼을 수 없습니다.

`event_id`는 예측 Feature가 아닌 추적용 ID입니다. Stratified 60/20/20 분할을 사용하며, 각 분할은 고정 Seed를 바탕으로 구성합니다.

### Fleet Events

6개 시설(S01~S06) × 시설당 설비 16대 × 8주로 총 768건입니다. 같은 설비는 여러 주에 기록됩니다. `site_id`는 시설, `device_id`는 설비, `week`는 검토 건수 제한을 계산하는 주차입니다.

- `equipment_type`: 설비 종류를 나타내는 0 또는 1
- `vibration`: 진동 측정값
- `temperature_c`: 온도
- `utilization`: 이용률(0~1)
- `days_since_service`: 직전 점검 이후 경과 일수
- `prior_alerts`: 이전에 발생한 경보 건수
- `maintenance_label`: 이후 정비가 필요했는지에 관한 정답 Label
- `post_inspection_result`: 현장 점검을 마친 뒤에만 얻을 수 있는 결과. **예측에 사용하면 Data Leakage** 임

Professional Project에서는 Train S01~S04, Validation S05, Test S06으로 **시설 단위 분할** 합니다. 같은 설비나 시설이 Train과 평가 데이터에 동시에 등장하지 않습니다. 단, 이 분할은 새로운 시설에 대한 일반화 점검이며 **미래 시점의 성능을 검증했다는 뜻은 아닙니다.** 시간 변화에 대한 별도 평가가 필요할 수 있습니다.

## 데이터 재생성

`Chapter-07/` 폴더에서 실행합니다.

```bash
python scripts/make_datasets.py
```

스크립트는 NumPy의 고정 Seed를 사용합니다. 같은 버전과 환경에서 CSV 결과를 재생성하도록 설계했으나, 라이브러리 버전과 실행 환경이 다르면 난수 구현·부동소수점 출력에 차이가 발생할 수 있습니다. CSV가 이미 포함되어 있으므로 재생성은 선택 사항입니다.

[← Chapter 07](../README.md)
