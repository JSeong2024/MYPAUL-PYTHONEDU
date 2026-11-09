[← Chapter 06](../README.md) · [Contents](../README.md#contents)

# 실습 데이터

이 폴더의 CSV는 모두 `scripts/make_datasets.py`로 생성한 **실습용 합성 데이터**입니다. 외부 서비스에서 수집한 실제 기록이 아닙니다. Seed는 42로 설정되어 있습니다.

| 파일 | 행 | 특징 | 용도 |
|---|---:|---|---|
| `xor_signals.csv` | 256 | `signal_x`, `signal_y`, `label` | 비선형 결정 경계 |
| `nonlinear_demand.csv` | 300 | 온도, 부하, 수요 | 비선형 회귀 |
| `triage_signals.csv` | 360 | `f1`~`f6`, `class_id` | 구조 비교와 모델 전달 |

`xor_signals.csv`의 Label은 두 입력 부호가 다르면 1입니다. `nonlinear_demand.csv`의 Target은 비선형 함수와 작은 난수를 합쳐 생성했습니다. `triage_signals.csv`의 Label은 Feature 간 상호작용을 포함한 합성 점수를 삼분위로 나눠 만들었습니다.

```bash
python scripts/make_datasets.py
```

스크립트는 동일한 파일을 다시 생성하므로 CSV 내용을 수정한 경우 별도로 백업하세요. 평가 데이터 분할은 프로젝트 실행 단계에서 별도로 수행합니다.
