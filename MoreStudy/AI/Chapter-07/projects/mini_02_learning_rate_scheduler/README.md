[← Chapter 07](../../README.md) · [Projects](../../README.md#section-7-20)

# Mini Project 02. Learning Rate Scheduler — Alert Classification

## 문제 상황

설비 경보 여부를 분류하는 모델에서 고정 Learning Rate와 StepLR을 비교합니다. Scheduler를 사용했다는 사실만으로 성능 개선을 주장하지 않고, 실제 사용된 LR과 Validation Loss를 함께 기록합니다.

## 입력 데이터

[`device_alerts.csv`](../../data/device_alerts.csv) — 420건. Feature: `vibration`, `temperature_c`, `load_factor`, `days_since_service`; Label: `alert_label`(0/1), ID: `event_id`. 실습용 합성 데이터입니다.

## 요구사항

1. Stratified Train(60%)·Validation(20%)·Test(20%)로 분리하고 Train에서만 Scaling 통계량을 계산합니다.
2. `Linear(4,16) → ReLU → Linear(16,1)` 모델과 동일한 초기 Weight로 시작합니다.
3. 두 실험 모두 SGD(`lr=0.085`, `momentum=0.85`)와 `BCEWithLogitsLoss`를 사용합니다.
4. 첫 실험은 LR을 고정하고, 두 번째는 `StepLR(step_size=8, gamma=0.5)`를 적용합니다.
5. 28 Epoch 동안 실제 사용한 LR, Train Loss, Validation Loss를 기록합니다. Scheduler는 Epoch의 Optimizer 갱신을 마친 후 호출합니다.
6. Validation Loss가 가장 낮은 Weight로 복원한 후 Test Accuracy와 F1을 계산합니다.

## 출력 파일

| 파일 | 내용 |
|---|---|
| `scheduler_comparison.csv` | 두 학습 정책의 Best Epoch, Validation Loss, Test Accuracy·F1 |
| `learning_rate_history.csv` | Epoch별 LR과 Loss |

## 구현 가이드

`optimizer.param_groups[0]["lr"]`은 해당 Epoch에서 실제 사용할 Learning Rate입니다. `scheduler.step()`은 Optimizer 갱신 후 호출하고, `best_state`를 보관하세요.

## 검증 기준

- 첫 두 Epoch에서 실험 간 초기 Weight가 같습니다.
- StepLR의 변경 시점이 올바릅니다.
- Sigmoid는 확률 산출 시에만 적용하고 Loss에는 Logits를 직접 전달합니다.
- Test에서 학습률을 선택하지 않습니다.

## 테스트 시나리오

| 항목 | 확인 내용 |
|---|---|
| Scheduler 시점 | 8번째 Epoch까지 LR 0.085, 9번째부터 0.0425 |
| 고정 LR | 고정 실험에서는 Epoch별 LR이 0.085 |
| 분할 독립성 | 동일 행이 Train·Validation·Test에 중복되지 않는지 확인 |
| Label 유효성 | `alert_label`에 0·1 이외 값이 들어오면 거부 |

## 실행 방법

Chapter-07/ 디렉터리에서 실행합니다.

```bash
python projects/mini_02_learning_rate_scheduler/starter.py
python solutions/mini_02_learning_rate_scheduler.py
python -m unittest discover -s tests -v
```

학생용 Starter는 TODO가 남아 있어 완료하기 전에는 `NotImplementedError`가 발생합니다. 모범 구현을 먼저 확인하지 않고 요구사항에 맞춰 작성해 보세요.

모범 구현: [`solutions/mini_02_learning_rate_scheduler.py`](../../solutions/mini_02_learning_rate_scheduler.py)

[← Chapter 07](../../README.md) · [Contents](../../README.md#contents)
