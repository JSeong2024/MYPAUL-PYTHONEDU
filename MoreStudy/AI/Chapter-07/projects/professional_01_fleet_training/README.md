[← Chapter 07](../../README.md) · [Projects](../../README.md#section-7-20)

# Professional Project 01. Fleet Risk Training — Validation Policy & Model Handoff

## 문제 상황

여섯 시설에 배치된 설비의 정비 위험을 예측하는 시스템을 준비합니다. 실제 운영팀이 확인할 수 있는 건수는 주차별 전체 이벤트의 30% 수준으로 제한됩니다. 새로운 시설에 적용할 수 있는지 평가하기 위해 시설 단위로 데이터를 분리하고, 예측 당시 알 수 없던 Feature를 제외하며, Validation에서 정책을 확정해야 합니다. 실제 안전 결정을 자동화하는 도구가 아니라 분석 역량을 점검하기 위한 실습입니다.

## 입력 데이터

[`fleet_events.csv`](../../data/fleet_events.csv) — 768건(시설 6개 × 설비 16개 × 8주). `site_id`, `device_id`, `event_id`, `week`, 예측 가능한 Feature, `maintenance_label`(0/1), `post_inspection_result`(사후 정보)를 포함합니다. 상세 열 정의는 [`data/README.md`](../../data/README.md)를 참고하세요.

## 요구사항

1. 기본 Schema, ID 중복, 결측값, 무한대, 이진 Label을 검사하고 잘못된 파일은 처리하지 않습니다.
2. Train 시설 S01~S04(512건), Validation S05(128건), Test S06(128건)로 분할합니다. 같은 시설의 기록이 서로 다른 Split에 포함되면 안 됩니다.
3. 예측 시점에 존재하지 않는 `post_inspection_result`, Target 자체 및 ID를 Feature에서 제외합니다. Feature 순서를 고정합니다.
4. Train만으로 평균과 표준편차를 계산하고, Label 불균형을 Train의 `pos_weight`로 반영합니다.
5. Linear와 MLP 후보를 학습합니다. AdamW, Gradient Clipping, Validation Loss에 따른 Early Stopping을 사용합니다.
6. Validation에서 `0.10~0.95`의 Threshold를 탐색합니다. 각 주차별 검토 건수는 `ceil(주차 Sample 수 × 0.30)` 이하여야 합니다. 이 범위 안에서 F2가 최대인 정책을 선택합니다.
7. Validation F2를 기준으로 후보 모델과 Threshold를 확정한 후, Test에서 F2·Precision·Recall, 검토 비율, 주차별 용량 초과 여부를 평가합니다.
8. 최종 Weight·Feature 순서·Scaling·Threshold를 저장하고, 복원한 모델의 Test 확률이 원본과 일치하는지 검증합니다.
9. 장비 유형별 Recall 차이를 함께 보고하고, 높은 점수만으로 실제 정비 자동화를 정당화하지 않습니다.

## 출력 파일

| 파일 | 내용 |
|---|---|
| `candidate_scores.csv` | 후보 모델, Best Epoch, Validation Loss, F2, 검토 비율 |
| `training_history.csv` | 모델·Epoch별 Train·Validation Loss |
| `test_predictions.csv` | Test 이벤트 ID, 시설, 주차, 실제 Label, 위험 점수, 검토 여부 |
| `model_weights.pt` | 선택된 모델의 Weight |
| `metadata.json` | 모델 종류·Feature 순서·Train Scaling·Threshold |
| `evaluation.json` | Split 크기, 운영 지표, 주차별 용량 초과, 유형별 Recall |

## 구현 가이드

DataFrame에서 명시적 Feature 리스트를 만들고 `df[FEATURES]` 순서를 고정합니다. 정책 선택 함수는 Validation의 실제 Label·확률·주차만 받아야 하며, 최종 Test 호출은 모델 선택을 마친 후로 둡니다.

## 검증 기준

- Train/Validation/Test의 시설 ID가 서로 겹치면 안 됩니다.
- `post_inspection_result`를 넣어 높은 점수를 얻으면 실격입니다.
- Validation으로 선택한 Threshold를 Test에서 다시 조정하지 않습니다.
- 주차별 검토 가능 건수는 Validation에서는 제약으로, Test에서는 관측 결과로 다룹니다.
- 복원된 모델의 예측 차이는 `1e-6` 이내여야 합니다.
- 실패한 데이터 검증 뒤에는 부정확한 보고서를 성공한 결과처럼 출력하지 않습니다.

## 테스트 시나리오

| 항목 | 확인 내용 |
|---|---|
| 입력 오류 | 중복 `event_id`·누락된 필수 열·무한대가 있으면 실행 거부 |
| 시설 분할 | S01~S04 / S05 / S06 사이에 시설 ID가 겹치지 않음 |
| Leakage | `post_inspection_result`와 Target이 Feature에 포함되지 않음 |
| 검토 용량 | Validation 각 Week의 검토 건수가 `ceil(0.3 × week_count)` 이하 |
| 정책 고정 | Test에서는 확정된 Threshold를 변경하지 않고 초과 여부만 보고 |
| 복원 일치 | 저장·복원 모델의 확률 차이가 1e-6 이내 |

## 실행 방법

Chapter-07/ 디렉터리에서 실행합니다.

```bash
python projects/professional_01_fleet_training/starter.py
python solutions/professional_01_fleet_training.py
python -m unittest discover -s tests -v
```

학생용 Starter는 TODO가 남아 있어 완료하기 전에는 `NotImplementedError`가 발생합니다. 모범 구현을 먼저 확인하지 않고 요구사항에 맞춰 작성해 보세요.

모범 구현: [`solutions/professional_01_fleet_training.py`](../../solutions/professional_01_fleet_training.py)

[← Chapter 07](../../README.md) · [Contents](../../README.md#contents)
