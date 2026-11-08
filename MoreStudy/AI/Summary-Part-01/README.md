# Summary — Part 01. AI & Machine Learning Fundamentals

Chapter 01부터 04까지 학습한 AI의 개념, 머신러닝의 기본 원리, 학습 방식과 모델 평가를 종합적으로 점검하는 문제집입니다. Quiz로 핵심 개념과 코드 해석 능력을 확인하고, Problems에서 데이터 처리부터 모델 설계·검증까지 단계적으로 다룹니다.

## Contents

| 자료 | 구성 |
|:---|:---|
| [Quiz](./quiz.md) | 객관식 16문항, 주관식 8문항과 정답 및 해설 |
| [Problems](./problem.md) | Basic 5, Advanced 4, Professional 3, Challenge 2, Radiant 1문제 |
| [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/AI/Summary-Part-01/Summary-Part-01.html) | 문제 탐색, 객관식 채점, 답안 작성 및 해설·구현 가이드 |
| [학생용 코드](./exercises/) | 15문항의 미완성 Python 코드 |
| [모범답안](./solutions/) | 문제별 실행 가능한 구현과 공통 검증 함수 |
| [자동 검증](./tests/check.py) | 예제, 파일 결과, 분할·누수, 장애 복구 검증 |
| [실습 데이터](./data/) | 프로젝트 실행에 필요한 실습용 합성 데이터 |

## Getting Started

[HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/AI/Summary-Part-01/Summary-Part-01.html)에서 Quiz와 Problems를 선택할 수 있습니다. 객관식은 답안을 선택한 뒤 채점하고, 주관식은 모범답안과 비교합니다. Problems는 난이도별로 문제를 탐색하고 입력·출력 조건과 검증 기준을 확인할 수 있습니다.

브라우저에서 실행하는 HTML 파일은 별도의 설치가 필요하지 않습니다. 오프라인에서는 `Summary-Part-01.html` 파일을 직접 열어 사용할 수 있습니다. 작성한 답안은 브라우저의 로컬 저장 공간에 보관되므로 다른 브라우저나 기기와 자동 동기화되지 않습니다.

Python 실습에서는 저장소의 `MoreStudy/AI/Summary-Part-01/` 폴더를 작업 기준으로 사용합니다. Python 3.11 이상을 권장합니다. Google Colab에서는 Chapter 폴더를 업로드하거나 드라이브에서 연 뒤 같은 파일을 실행할 수 있습니다.

```bash
python -m pip install -r requirements.txt
python tests/run_solution.py B-01
python tests/run_solution.py A-03
python tests/run_solution.py R-01
python tests/check.py
```

`run_solution.py`는 문제에 필요한 입력 파일을 `outputs/문제번호/`로 복사한 후 모범 구현을 실행합니다. 생성된 CSV·JSON·보고서도 같은 폴더에서 확인할 수 있습니다. C-02와 R-01은 이전 정상 결과를 보호하기 위해 해당 작업 폴더의 `results/` 아래에 결과물을 생성합니다.

직접 구현하려면 `exercises/문제번호.py`의 `TODO`를 완성하세요. Starter Code는 의도적으로 미완성이며, 자동 테스트는 `solutions/`의 모범 구현을 검사합니다. 모범답안을 실행하기 전에 문제의 입력·출력 규격을 먼저 확인하는 것을 권장합니다.

합성 데이터는 `data/문제번호/`에 포함되어 있습니다. 입력 데이터를 다시 생성하려면 다음 명령을 사용합니다. 기존 데이터를 덮어쓰므로 변경한 파일은 먼저 별도 보관하세요.

```bash
python tests/generate_data.py --output data
```

실습용 CSV는 실제 시설·설비 기록이 아닌 합성 데이터입니다. 라이브러리 버전과 모델 특성에 따라 일부 실수형 성능 지표는 달라질 수 있으므로, 고정 점수보다는 데이터 분할과 계산 규칙을 기준으로 확인합니다.

## Learning Scope

| Chapter | 주제 |
|:---:|---|
| [01](../Chapter-01/README.md) | AI 개념, Rule-Based Systems, Training과 Inference, AI의 활용과 한계 |
| [02](../Chapter-02/README.md) | Feature, Target, Linear Regression, Loss Function, Gradient Descent, Scaling, Data Leakage |
| [03](../Chapter-03/README.md) | Supervised·Unsupervised Learning, Classification, KMeans, DBSCAN |
| [04](../Chapter-04/README.md) | Evaluation Metrics, Cross-Validation, Pipeline, Hyperparameter Tuning, Group·Temporal Evaluation |

## Problems

| 난이도 | 문제 수 | 평가 내용 |
|---|---:|---|
| Basic | 5 | 주요 개념과 기본 계산의 정확한 구현 |
| Advanced | 4 | 데이터 처리 흐름, 모델 적용 및 결과 해석 |
| Professional | 3 | 실무 요구사항에 맞는 프로젝트·평가 절차 설계 |
| Challenge | 2 | 운영 장애의 원인 분석, 복구 및 재발 방지 |
| Radiant | 1 | 복합 분석 시스템의 신뢰성·효율·평가 체계 설계 |

문제는 Chapter 01~04를 기준으로 하며, 필요한 경우 Python, NumPy, Pandas, scikit-learn을 활용할 수 있습니다. PyTorch나 딥러닝은 요구하지 않습니다. 각 Problem의 입력·출력과 검증 기준을 먼저 확인한 뒤 구현 가이드를 참고하세요.

## Directory Structure

```text
Summary-Part-01/
├── README.md
├── Summary-Part-01.html
├── quiz.md
├── problem.md
├── requirements.txt
├── .gitignore
├── data/              # 실습용 합성 데이터
├── exercises/         # B-01.py ~ R-01.py (Starter Code)
├── solutions/         # 모범 구현 15개, 공통 유틸리티, Radiant 참고 문서
└── tests/
    ├── check.py
    ├── generate_data.py
    └── run_solution.py
```

---

[← AI 목차](../README.md#contents) · [Quiz](./quiz.md) · [Problems](./problem.md) · [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/AI/Summary-Part-01/Summary-Part-01.html)
