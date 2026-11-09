[← Chapter 07](../../README.md) · [Projects](../../README.md#section-7-20)

# Mini Project 01. Optimizer Comparison — Energy Demand

## 문제 상황

시간대·기온·이용량에 따른 전력 수요를 추정하는 신경망을 학습합니다. 같은 모델을 같은 초기 Weight에서 시작해 SGD Momentum과 AdamW가 어떻게 다른 학습 경로를 보이는지 확인합니다. 특정 Optimizer가 언제나 우수하다고 단정하지 않고 Validation과 Test를 분리해 비교합니다.

## 입력 데이터

[`energy_demand.csv`](../../data/energy_demand.csv) — 시간 순서 360건. Feature는 `hour`, `temperature_c`, `occupancy`, `is_weekend`, Target은 `demand_kwh`, 추적 ID는 `observation_id`입니다. 모두 실습용 합성 데이터입니다.

## 요구사항

1. 시간 순서대로 처음 240건을 Train, 다음 60건을 Validation, 마지막 60건을 Test로 사용합니다.
2. Train의 평균·표준편차만으로 Feature와 Target을 Scaling합니다. 표준편차가 0이면 1로 대체합니다.
3. `Linear(4,24) → ReLU → Linear(24,1)` 구조와 초기 Weight를 동일하게 유지합니다.
4. SGD(`lr=0.045`, `momentum=0.85`)와 AdamW(`lr=0.012`, `weight_decay=0`)를 각각 36 Epoch 학습합니다.
5. 각 Epoch의 Train·Validation MSE를 기록하며, Validation Loss가 가장 낮았던 Weight를 복원합니다.
6. 설정이 모두 확정된 후 Test MAE·RMSE를 원래 kWh 단위로 계산하고 예측 CSV를 저장합니다.

## 출력 파일

| 파일 | 내용 |
|---|---|
| `optimizer_comparison.csv` | Optimizer 이름, Best Epoch, Validation MSE, Test MAE·RMSE |
| `training_history.csv` | Optimizer, Epoch, Train·Validation Loss, Learning Rate |
| `test_predictions.csv` | ID, 실제 수요, 두 Optimizer의 예측 수요 |

## 구현 가이드

`copy.deepcopy(model.state_dict())`로 공통 초기 Weight와 Best Weight를 별도로 보관합니다. `optimizer.zero_grad(set_to_none=True)` → Forward → Loss → Backward → Step 순서를 유지합니다.

## 검증 기준

- 같은 초기 Weight에서 출발해야 합니다.
- Scaling에 Validation·Test 데이터를 사용하지 않습니다.
- 두 Optimizer의 Test 결과는 마지막에 한 번만 계산합니다.
- 각 Epoch의 Loss와 Best Epoch를 비교할 수 있어야 합니다.

## 테스트 시나리오

| 항목 | 확인 내용 |
|---|---|
| 공통 초기 Weight | 각 Optimizer 실행 직전 Parameter가 일치하는지 확인 |
| 시간 순서 Split | Train 240·Validation 60·Test 60 유지 |
| 불완전한 입력 | `demand_kwh` 누락 또는 NaN이면 실행 중단 |
| Metric 단위 | 최종 MAE·RMSE를 원래 kWh 단위로 보고 |

## 실행 방법

Chapter-07/ 디렉터리에서 실행합니다.

```bash
python projects/mini_01_optimizer_comparison/starter.py
python solutions/mini_01_optimizer_comparison.py
python -m unittest discover -s tests -v
```

학생용 Starter는 TODO가 남아 있어 완료하기 전에는 `NotImplementedError`가 발생합니다. 모범 구현을 먼저 확인하지 않고 요구사항에 맞춰 작성해 보세요.

모범 구현: [`solutions/mini_01_optimizer_comparison.py`](../../solutions/mini_01_optimizer_comparison.py)

[← Chapter 07](../../README.md) · [Contents](../../README.md#contents)
