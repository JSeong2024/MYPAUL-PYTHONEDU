# Summary — Part 02. Deep Learning with PyTorch

Chapter 05~07에서 학습한 Tensor 연산, 자동 미분, 신경망 구성, 모델 학습과 최적화를 종합적으로 점검합니다.

## Contents

| 자료 | 구성 | 문제 수 |
|---|---|---:|
| [Quiz](./quiz.md) | 객관식 16문항 · 주관식 8문항, 정답 및 해설 | 24 |
| [Problems](./problem.md) | Basic 5 · Advanced 4 · Professional 3 · Challenge 2 · Radiant 1 | 15 |
| [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/AI/Summary-Part-02/Summary-Part-02.html) | 문제 탐색, 선택한 객관식 채점, 단계별 HELP | 39 |
| **전체** | | **39** |

## 학습 범위

- [Chapter 05 — PyTorch Fundamentals](../Chapter-05/README.md): Tensor, Broadcasting, Device, Autograd, Dataset·DataLoader, Gradient 관리
- [Chapter 06 — Neural Networks & Deep Learning](../Chapter-06/README.md): `nn.Module`, MLP, Activation, Forward·Backward, Loss, Train·Eval, 모델 저장
- [Chapter 07 — Model Training & Optimization](../Chapter-07/README.md): Optimizer, Scheduler, Early Stopping, Regularization, Gradient Accumulation·Clipping, Checkpoint, Reproducibility

Chapter 01~04에서 다룬 데이터 분할과 평가 지표는 선행 지식으로 활용합니다. CNN, Transformer 및 대규모 모델 학습은 포함하지 않습니다.

## 진행 안내

Quiz에서는 핵심 개념의 이해, 코드 실행 결과의 해석, 올바른 학습 절차를 구분하는 능력을 확인합니다. 객관식은 문항마다 정답이 하나이며, 주관식은 계산 과정이나 판단 근거를 작성한 뒤 모범답안과 비교할 수 있습니다. 정답과 해설은 각 문항의 접기 영역에서 확인할 수 있습니다.

Problems는 요구사항과 입출력 규격에 맞는 Python 프로그램을 작성하는 과제입니다. 모델의 성능 지표만으로 완성도를 판단하지 않으며, 데이터 무결성, 학습·평가 분리, 실행 재현성 및 오류 처리도 검증합니다.

| 단계 | 평가 관점 |
|---|---|
| Basic | Tensor와 기본 신경망 연산을 정확하게 구현하는 능력 |
| Advanced | 데이터 처리·학습·평가·추론을 연결하는 능력 |
| Professional | 실제 프로젝트의 학습 파이프라인과 운영 기준을 설계하는 능력 |
| Challenge | 학습 중단·예측 장애를 진단하고 안전하게 복구하는 능력 |
| Radiant | 학습·평가·배포·복구를 통합하고 시스템의 신뢰성과 성능을 함께 검증하는 능력 |

별도 언급이 없는 문제는 **CPU 환경에서 실행할 수 있도록** 구성했습니다. GPU 사용은 선택 사항이며 필수 조건은 아닙니다. 재현성이 필요한 문제에는 Seed, 데이터 순서 및 허용 오차를 명시합니다. 난수에 따라 달라지는 학습 점수를 고정된 정답으로 취급하지 않습니다.

문제에 사용하는 CSV는 모두 **실습용 합성 데이터**입니다. 입력 데이터의 열 구성과 유효성 조건은 각 문제에 명시되어 있습니다.

## 실행 방법

브라우저에서 [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/AI/Summary-Part-02/Summary-Part-02.html)을 열거나, 저장소의 `Summary-Part-02.html`을 실행할 수 있습니다. HTML에는 실행 결과 그래프가 포함되어 있으며, 코드 실습은 Python 환경에서 진행합니다.

저장소의 `MoreStudy/AI/Summary-Part-02/` 디렉터리를 기준으로 실행합니다.

```bash
python -m pip install -r requirements.txt
python tests/run_solution.py A-02
python tests/run_solution.py P-03
python tests/run_solution.py R-01
python tests/check.py
```

Basic 문제는 표준 입력을 사용합니다. 예를 들어 B-04는 다음과 같이 실행할 수 있습니다.

```bash
python solutions/B-04.py
# 입력 예: 5 3 4 2
```

`exercises/`에는 학생용 미완성 코드, `solutions/`에는 모범 구현이 있습니다. 학습 중 생성되는 결과물은 `outputs/문제번호/`에 저장되며, GitHub 배포 파일에는 포함하지 않습니다. 입력 데이터는 [`data/README.md`](./data/README.md)에 정리했습니다.

## 파일 구성

```text
Summary-Part-02/
├── README.md
├── quiz.md
├── problem.md
├── Summary-Part-02.html
├── requirements.txt
├── data/               # 실습용 합성 데이터
├── assets/problems/    # 실제 모범 구현 결과 그래프
├── exercises/          # B-01.py ~ R-01.py
├── solutions/          # 문제별 정답 코드 및 공통 모듈
└── tests/              # 데이터 생성, Solution 실행, 자동 검증
```

각 Problem의 요구사항과 검증 기준은 [`problem.md`](./problem.md)를 확인합니다. 모델 평가 결과와 실행 시간은 합성 데이터와 실행 환경에 따라 달라질 수 있으므로 모든 학습 점수를 고정된 정답으로 비교하지 않습니다.

---

[Quiz 풀기](./quiz.md) · [Problems 풀기](./problem.md) · [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/AI/Summary-Part-02/Summary-Part-02.html) · [AI 목차](../README.md)
