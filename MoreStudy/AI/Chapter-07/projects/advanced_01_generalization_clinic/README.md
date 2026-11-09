[← Chapter 07](../../README.md) · [Projects](../../README.md#section-7-20)

# Advanced Project 01. Generalization Clinic — Early Stopping & Regularization

## 문제 상황

작은 Training Set으로 비교적 큰 MLP를 학습하면 Training Loss는 낮아져도 Validation 성능이 나빠질 수 있습니다. Early Stopping과 Regularization을 적용해 학습 기록을 분석하고, 성능이 좋아졌는지 근거를 제시합니다.

## 입력 데이터

[`energy_demand.csv`](../../data/energy_demand.csv) — 처음 240개 Train 후보에서 네 번째 Sample마다 하나씩 뽑아 60개로 제한합니다. Validation은 241~300번째, Test는 301~360번째 Sample입니다. Scaling 기준은 원래 Train 구간 240건에서 계산합니다.

## 요구사항

1. `Linear(4,64) → ReLU → Dropout(p) → Linear(64,1)` 구조를 사용합니다.
2. `unregularized`는 Dropout=0, Weight Decay=0으로 설정합니다.
3. `regularized`는 Dropout=0.15, AdamW Weight Decay=0.05를 사용합니다.
4. 각 모델을 최대 75 Epoch 학습하고, Validation Loss가 10 Epoch 연속 개선되지 않으면 중단합니다.
5. 최저 Validation Loss의 Weight와 Epoch를 저장합니다. Train·Validation 곡선을 기록합니다.
6. 복원된 Weight로 Test MAE를 한 번 계산합니다. Regularization의 효과는 실제 결과에 근거해 해석합니다.

## 출력 파일

| 파일 | 내용 |
|---|---|
| `generalization_summary.csv` | 모델 설정, Best Epoch, 학습 Epoch, Best Validation Loss, Test MAE |
| `learning_curves.csv` | Epoch별 Train·Validation Loss |
| `test_predictions.csv` | 각 모델의 Test 예측값 |

## 구현 가이드

`model.train()`과 `model.eval()`을 구분해야 Dropout 실험이 성립합니다. Best Weight는 `copy.deepcopy`로 보관해야 이후 Epoch에서 변경되지 않습니다.

## 검증 기준

- Validation 기준으로 Early Stopping합니다.
- Dropout과 Weight Decay의 역할을 구분합니다.
- 모든 설정에서 Regularization이 반드시 우수하다고 가정하지 않습니다.
- 결과 해석에서 Train과 Validation의 차이를 확인합니다.

## 테스트 시나리오

| 항목 | 확인 내용 |
|---|---|
| 제한된 Train | 60개 Sample만 Parameter 학습에 사용 |
| Patience | Validation 개선이 없을 때 지정한 Epoch 이후 종료 |
| Best Weight | 마지막 Epoch가 아닌 최소 Validation Loss의 State를 복원 |
| 정직한 비교 | Regularization이 늘 우수하다고 가정하지 않고 실제 Metric을 비교 |

## 실행 방법

Chapter-07/ 디렉터리에서 실행합니다.

```bash
python projects/advanced_01_generalization_clinic/starter.py
python solutions/advanced_01_generalization_clinic.py
python -m unittest discover -s tests -v
```

학생용 Starter는 TODO가 남아 있어 완료하기 전에는 `NotImplementedError`가 발생합니다. 모범 구현을 먼저 확인하지 않고 요구사항에 맞춰 작성해 보세요.

모범 구현: [`solutions/advanced_01_generalization_clinic.py`](../../solutions/advanced_01_generalization_clinic.py)

[← Chapter 07](../../README.md) · [Contents](../../README.md#contents)
