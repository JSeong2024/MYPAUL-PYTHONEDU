[← Chapter 07](../../README.md) · [Projects](../../README.md#section-7-20)

# Advanced Project 02. Gradient Accumulation & Clipping Audit

## 문제 상황

가용 메모리가 작은 환경에서 11개의 Sample을 한 번에 처리하기 어렵다고 가정합니다. 4·4·3개로 나누어 Backward한 결과가 전체 11개 Sample을 한 번에 처리한 Gradient와 일치하는지 검증합니다. 이후 Gradient Clipping을 적용합니다.

## 입력 데이터

[`device_alerts.csv`](../../data/device_alerts.csv)에서 Stratified Train 분할의 첫 11개 Sample을 사용합니다. Train Scaling을 적용한 Feature 4개와 Binary Label을 사용하며 `nn.Linear(4,1)`로 Gradient를 계산합니다.

## 요구사항

1. `BCEWithLogitsLoss(reduction="mean")`를 사용합니다.
2. 전체 11개 Sample의 Loss를 한 번 Backward한 Gradient Vector를 계산합니다.
3. 동일한 초기 Weight에서 4·4·3개 Micro-Batch를 순회하고, 각 Micro-Batch의 평균 Loss에 `해당 Batch 크기 / 11`을 곱해 Backward합니다.
4. 두 방식의 Gradient 차이 최댓값을 계산하고 허용 오차 `1e-6` 이내인지 검증합니다.
5. 전체 Gradient가 누적된 뒤 `clip_grad_norm_(..., max_norm=0.3)`을 딱 한 번 수행합니다.
6. Clipping 전·후 Norm과 각 Parameter의 Gradient를 CSV 및 JSON으로 기록합니다.

## 출력 파일

| 파일 | 내용 |
|---|---|
| `gradient_audit.json` | Micro-Batch 크기, 최대 Gradient 차이, Clipping 전·후 Norm |
| `gradient_vectors.csv` | 각 Parameter의 Full/Micro/Clipped Gradient |

## 구현 가이드

평균 Loss는 미니 배치 크기가 다를 때 단순 합산하면 안 됩니다. `loss * len(x_batch) / len(x_all)`로 가중합니다.

## 검증 기준

- 마지막 3개 Sample의 Loss에 잘못된 가중치를 적용하지 않습니다.
- Micro-Batch마다 Optimizer Step을 실행하면 동일 Gradient 비교가 성립하지 않습니다.
- Clipping은 누적을 마친 후 실행합니다.

## 테스트 시나리오

| 항목 | 확인 내용 |
|---|---|
| 마지막 Micro-Batch | 11개 Sample을 정확히 4·4·3개로 처리 |
| Gradient 일치 | Full vs Accumulated Gradient의 최대 차이 1e-6 이하 |
| Clipping 시점 | 모든 Micro-Batch Backward가 끝난 뒤 한 번 적용 |
| 잘못된 인자 | `max_norm <= 0`이면 실행을 거부 |

## 실행 방법

Chapter-07/ 디렉터리에서 실행합니다.

```bash
python projects/advanced_02_gradient_audit/starter.py
python solutions/advanced_02_gradient_audit.py
python -m unittest discover -s tests -v
```

학생용 Starter는 TODO가 남아 있어 완료하기 전에는 `NotImplementedError`가 발생합니다. 모범 구현을 먼저 확인하지 않고 요구사항에 맞춰 작성해 보세요.

모범 구현: [`solutions/advanced_02_gradient_audit.py`](../../solutions/advanced_02_gradient_audit.py)

[← Chapter 07](../../README.md) · [Contents](../../README.md#contents)
