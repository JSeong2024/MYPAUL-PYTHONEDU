[← Chapter 07](../../README.md) · [Projects](../../README.md#section-7-20)

# Advanced Project 03. Checkpoint & Exact Resume

## 문제 상황

학습이 5번째 Epoch 이후 중단됐다고 가정합니다. 모델 Weight만 복원하면 AdamW의 내부 상태나 Scheduler 위치가 사라져 같은 학습을 재현할 수 없습니다. 필요한 상태를 저장하고 정확히 이어 학습하는 방법을 구현합니다.

## 입력 데이터

[`energy_demand.csv`](../../data/energy_demand.csv)의 Train(240)·Validation(60)을 사용합니다. Test는 이 프로젝트에서 사용하지 않습니다.

## 요구사항

1. `Linear(4,20) → Tanh → Linear(20,1)`, AdamW(`lr=0.014`, `weight_decay=0.01`), StepLR(`step_size=4`, `gamma=0.75`)을 설정합니다.
2. 12 Epoch를 중단 없이 학습한 Weight와 Loss 기록을 보관합니다.
3. 동일한 초기 Weight에서 5 Epoch 학습 후 모델·Optimizer·Scheduler 상태, 완료 Epoch, 전처리 통계량을 Checkpoint로 저장합니다.
4. `torch.load(..., weights_only=True)`로 자신이 생성한 Checkpoint를 불러옵니다.
5. 6번째 Epoch부터 12번째 Epoch까지 학습하고, 12 Epoch 연속 실행 결과와 Parameter 및 Validation Loss를 비교합니다.
6. Shuffle은 `seed=1000+epoch` 방식으로 동일한 Batch 순서를 재현하도록 합니다.

## 출력 파일

| 파일 | 내용 |
|---|---|
| `checkpoint.pt` | 5 Epoch 완료 직후의 모델·Optimizer·Scheduler 상태 |
| `resume_history.csv` | 연속 실행과 재개 실행의 Epoch별 Loss 및 LR |
| `resume_report.json` | 최종 Parameter와 Validation Loss의 차이 |

## 구현 가이드

`torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(), "epoch": epoch}, path)`처럼 여러 상태를 보관합니다. Shuffle 재현 조건도 필요합니다.

## 검증 기준

- 같은 환경에서 최종 Parameter 최대 차이 `1e-7` 이하를 목표로 합니다.
- Scheduler와 Optimizer 상태를 둘 다 복원합니다.
- Checkpoint는 신뢰할 수 있는 로컬 파일만 불러옵니다.
- Checkpoint를 Test 성능에 맞춰 선택하지 않습니다.

## 테스트 시나리오

| 항목 | 확인 내용 |
|---|---|
| 모델 재개 | 중단 시점에서 Model·Optimizer·Scheduler를 모두 복원 |
| 정확도 비교 | 12 Epoch 연속 실행과 재개 실행의 Parameter 최대 차이 1e-7 이하 |
| 잘못된 분할 Epoch | `split_epoch >= total_epochs`이면 오류 |
| State 안전성 | 로컬 Checkpoint를 `weights_only=True`로 로드 |

## 실행 방법

Chapter-07/ 디렉터리에서 실행합니다.

```bash
python projects/advanced_03_checkpoint_resume/starter.py
python solutions/advanced_03_checkpoint_resume.py
python -m unittest discover -s tests -v
```

학생용 Starter는 TODO가 남아 있어 완료하기 전에는 `NotImplementedError`가 발생합니다. 모범 구현을 먼저 확인하지 않고 요구사항에 맞춰 작성해 보세요.

모범 구현: [`solutions/advanced_03_checkpoint_resume.py`](../../solutions/advanced_03_checkpoint_resume.py)

[← Chapter 07](../../README.md) · [Contents](../../README.md#contents)
