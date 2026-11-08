<p align="center">
  <img src="banner_AI.png" width="50%" alt="Artificial Intelligence Class Banner">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Google_Colab-F9AB00?style=flat&logo=googlecolab&logoColor=white" alt="Google Colab">
  <img src="https://img.shields.io/badge/Jupyter_Notebook-F37626?style=flat&logo=jupyter&logoColor=white" alt="Jupyter Notebook">
</p>

# Artificial Intelligence

Python을 기반으로 인공지능(Artificial Intelligence, AI)의 기본 원리부터 머신러닝(Machine Learning), 딥러닝(Deep Learning), 생성형 AI와 모델 활용까지 단계적으로 학습하는 자료입니다. 모델을 사용하는 방법뿐 아니라 **데이터에서 무엇을 학습하는지, 예측 결과를 어떻게 평가하는지, 어떤 한계가 있는지**를 이해하는 데 중점을 둡니다.

처음 접하는 학습자도 따라갈 수 있도록 개념을 순서대로 설명하고, 수식이 필요한 부분은 기호의 의미와 간단한 계산 예제, Python 코드로 연결합니다. 이후 PyTorch를 이용한 모델 학습과 컴퓨터 비전·자연어 처리·대규모 언어 모델(LLM) 응용으로 확장합니다.

- **주요 언어:** Python
- **주요 라이브러리:** NumPy, Pandas, Matplotlib, scikit-learn, PyTorch, Hugging Face Transformers
- **권장 실행 환경:** Google Colab(기본), Visual Studio Code·Anaconda/Jupyter Notebook(로컬)
- **권장 선행 학습:** Python 기본 문법, 함수, 리스트·딕셔너리, NumPy 배열과 Pandas DataFrame
- **학습 자료:** 개념 설명, 수식과 계산 예제, 실행 코드, 연습문제, Mini·Advanced Project, Quiz 및 정답·해설

## Contents

### Part 1 — AI & ML Fundamentals

AI와 머신러닝의 차이를 이해하고, 데이터에서 규칙을 학습하는 과정과 기본적인 모델 평가 방법을 익힙니다.

| Chapter | Topic |
|:---:|---|
| 01 | **Introduction to Artificial Intelligence** — AI의 개념과 범위, 머신러닝·딥러닝의 관계, 활용 사례와 한계 |
| 02 | **Machine Learning Fundamentals** — 데이터와 특징(Feature), 학습·예측 흐름, 기본 모델과 손실 함수 |
| 03 | **Supervised & Unsupervised Learning** — 회귀·분류, 군집화, 데이터 분할과 학습 방식의 차이 |
| 04 | **Model Evaluation & Optimization** — 평가 지표, 과적합, 교차 검증, 하이퍼파라미터와 모델 개선 |

### Part 2 — Deep Learning with PyTorch

텐서와 자동 미분을 시작으로 신경망의 구조와 학습 과정을 직접 구현합니다.

| Chapter | Topic |
|:---:|---|
| 05 | **PyTorch Fundamentals** — Tensor, 연산, Autograd, Dataset과 DataLoader |
| 06 | **Neural Networks & Deep Learning** — 퍼셉트론, 활성화 함수, 다층 신경망, 순전파·역전파 |
| 07 | **Model Training & Optimization** — Loss Function, Gradient Descent, Optimizer, 학습률과 학습 안정성 |

### Part 3 — Modern AI Architectures

이미지와 텍스트를 다루는 신경망 구조를 살펴보고, Transformer와 LLM의 핵심 원리까지 연결합니다.

| Chapter | Topic |
|:---:|---|
| 08 | **Computer Vision & CNN** — 이미지 데이터, 합성곱 신경망, 이미지 분류와 특징 추출 |
| 09 | **Natural Language Processing** — 텍스트 전처리, 토큰화, 임베딩과 언어 데이터의 표현 |
| 10 | **Transformers & Large Language Models** — Attention, Transformer 구조, 사전 학습과 텍스트 생성 |

### Part 4 — AI Applications & Engineering

사전 학습된 모델을 활용하고, 외부 자료를 연결하며, 평가 가능한 응용 프로그램으로 발전시킵니다.

| Chapter | Topic |
|:---:|---|
| 11 | **Pretrained Models & Fine-Tuning** — 사전 학습 모델 활용, 전이 학습, Fine-Tuning과 경량화 기법 |
| 12 | **Retrieval-Augmented Generation (RAG)** — 문서 분할, 임베딩, 검색, 검색 결과를 활용한 응답 생성 |
| 13 | **Model Inference, Evaluation & Deployment** — 추론 흐름, 품질·성능 평가, 모델 제공과 운영 시 고려사항 |

### Part 5 — Artificial Intelligence Project

앞서 배운 개념을 종합하여 데이터 준비부터 모델 개발·평가·응용까지 완성하는 프로젝트 과정입니다.

| Chapter | Topic |
|:---:|---|
| 14 | **AI Projects & Challenges** — 종합 프로젝트, 성능 개선, 모델 평가, 복합 문제 해결 |

## Learning Path

```text
AI 개념 이해 (Artificial Intelligence)
    ↓
데이터와 문제 정의 (Data & Problem Definition)
    ↓
머신러닝 기초 (Machine Learning)
    ↓
모델 학습과 평가 (Training & Evaluation)
    ↓
PyTorch와 신경망 (Deep Learning)
    ↓
이미지·텍스트 모델 (Computer Vision & NLP)
    ↓
Transformer와 LLM (Modern AI Architectures)
    ↓
사전 학습 모델 활용·RAG (AI Applications)
    ↓
추론·평가·배포 (Inference & Deployment)
    ↓
종합 프로젝트 (AI Projects & Challenges)
```

단순히 예측 결과가 나오는 코드를 실행하는 데 그치지 않고, **입력 데이터 → 학습 방법 → 평가 기준 → 결과 해석**의 연결을 확인합니다. 모델의 성능은 한 번의 실행 결과만으로 판단하지 않으며, 학습 데이터와 평가 데이터를 구분하고 잘못된 예측이 발생하는 조건도 살펴봅니다.

<details>
<summary><strong>권장 선행 학습 목록</strong></summary>

- [Python 기초 정리](../PythonGuide/) — 변수, 조건문, 반복문, 함수, 자료구조
- [Data Processing](../Data_Processing/) — NumPy, Pandas, 데이터 정제·변환
- [Data Visualization](../Data_Visualization/) — 분포·관계·추세의 시각화와 해석

AI 입문 자체에 위의 모든 Chapter를 완료할 필요는 없습니다. 다만 머신러닝 실습에서는 Python의 함수와 배열 연산, 데이터프레임 활용 능력이 도움이 됩니다.

</details>

## Getting Started

### 1. 실행 환경 선택

AI 실습은 **Google Colab을 기본 실행 환경**으로 사용합니다. 별도의 로컬 Python 설치 없이 Notebook을 실행할 수 있으며, GPU가 필요한 학습에서는 Colab의 가속기 환경을 선택할 수 있습니다. 로컬에서는 VS Code 또는 Anaconda·Jupyter Notebook을 사용할 수 있습니다.

| 환경 | 권장 용도 | 특징 |
|---|---|---|
| **Google Colab** (기본) | 머신러닝·딥러닝 모델 학습, GPU 실습 | 브라우저에서 실행하며 서버의 연산 자원을 이용합니다. GPU 사용은 가용성과 할당량에 따라 제한됩니다. |
| **Visual Studio Code** | Python 문법 학습, 소규모 실험, 프로젝트 개발 | 코드와 파일을 관리하기 좋으며, 연산은 기본적으로 로컬 PC에서 수행합니다. |
| **Anaconda + Jupyter Notebook** | 데이터 탐색, 실험 과정 기록, 로컬 Notebook 실습 | Conda 환경을 분리하여 데이터 분석과 모델 실험을 진행할 수 있습니다. |

기초 머신러닝과 작은 신경망은 CPU로도 실습할 수 있습니다. 반면 대규모 데이터나 딥러닝 모델은 GPU·메모리 사용량이 커질 수 있으므로, 학습 규모에 따라 실행 환경을 선택합니다. **Colab에서 GPU 런타임을 선택하더라도 코드가 GPU를 사용하도록 작성되어 있지 않으면 CPU에서 연산할 수 있습니다.**

### 2. Google Colab 실습 (권장)

1. [Google Colab](https://colab.research.google.com/)에 접속하여 새 Notebook을 생성합니다.
2. 코드 셀에 Python 코드를 입력하고 `Shift + Enter`로 실행합니다.
3. GPU가 필요한 실습에서는 **런타임 → 런타임 유형 변경 → 하드웨어 가속기**에서 GPU를 선택합니다. GPU가 필요하지 않다면 기본 CPU 런타임을 사용합니다.
4. 추가 라이브러리가 필요한 경우 Notebook의 코드 셀에서 설치합니다.

```python
%pip install numpy pandas matplotlib scikit-learn
```

기본 라이브러리가 이미 설치되어 있다면 재설치할 필요는 없습니다. Python과 PyTorch 실행 환경은 다음과 같이 확인합니다.

```python
import sys

print(sys.version)

try:
    import torch
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
except ImportError:
    print("PyTorch is not installed.")
```

**실습 데이터와 결과물 보관:** Colab의 실행용 파일 시스템은 런타임이 종료되거나 초기화되면 유지되지 않을 수 있습니다. Notebook은 Google Drive에 저장하고, 필요한 CSV·모델 가중치·결과 파일은 별도로 다운로드하거나 Drive 등 지속 저장소에 보관합니다. Notebook에서 Drive를 연결하는 경우에는 해당 Notebook 코드가 연결된 Drive 파일에 접근할 수 있으므로 신뢰할 수 있는 코드인지 확인해야 합니다.

**사용 제한:** 무료 Colab의 GPU·메모리·실행 시간은 보장되지 않으며 사용량과 가용성에 따라 달라집니다. GPU가 할당되지 않거나 실행이 중단되는 경우에는 모델·배치 크기를 줄이거나 CPU/로컬 환경으로 전환할 수 있습니다.

### 3. 로컬 개발 환경 (VS Code / Anaconda·Jupyter Notebook)

로컬 실행 시에는 Python 3.11 이상을 권장합니다. 사용하는 라이브러리의 버전 지원 여부는 별도로 확인합니다.

**VS Code — 가상환경 생성**

`AI/` 디렉터리에서 다음 명령을 실행합니다.

```bash
python -m venv .venv
```

**가상환경 활성화**

- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
- Windows Command Prompt: `.venv\Scripts\activate.bat`
- macOS·Linux: `source .venv/bin/activate`

VS Code에서 해당 가상환경의 Python 인터프리터를 선택합니다. 가상환경 종료 명령은 `deactivate`입니다.

**Anaconda — Conda 환경 생성**

```bash
conda create -n mypaul-ai python=3.11
conda activate mypaul-ai
python -m pip install numpy pandas matplotlib scikit-learn notebook
jupyter notebook
```

VS Code의 `.venv`와 Conda 환경 중 **하나를 선택**하여 사용합니다. `.venv/` 및 개인별 환경 설정 파일은 저장소에 업로드하지 않습니다.

### 4. 기본 라이브러리 설치

로컬 터미널에서는 다음 명령을 실행합니다.

```bash
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib scikit-learn
```

Colab에서는 필요한 라이브러리만 `%pip install ...`로 설치할 수 있습니다. 환경이 기본 제공하는 라이브러리는 그대로 사용해도 됩니다.

| 라이브러리 | 주요 용도 |
|---|---|
| `numpy` | 배열과 수치 연산 |
| `pandas` | 데이터 조회·전처리·분석 |
| `matplotlib` | 데이터와 학습 결과 시각화 |
| `scikit-learn` | 머신러닝 모델, 데이터 분할, 평가 지표 |
| `torch` | 텐서·자동 미분·딥러닝 모델 학습 |
| `transformers` | 사전 학습된 Transformer 모델 활용 |

PyTorch는 운영체제와 CPU·GPU 환경에 따라 설치 명령이 달라질 수 있으므로 [PyTorch 설치 안내](https://pytorch.org/get-started/locally/)를 참고합니다. `torch`, `transformers` 등 추가 라이브러리는 해당 Chapter에서 필요한 시점에 설치합니다.

### 5. 첫 번째 머신러닝 예제

다음 코드는 **Colab과 로컬 Python 환경에서 동일하게 실행**할 수 있는 분류 예제입니다. 꽃의 측정값을 이용해 품종을 분류하며, scikit-learn에 포함된 Iris 데이터셋을 사용하므로 별도 CSV 파일이 필요하지 않습니다. K-최근접 이웃(K-Nearest Neighbors, KNN) 모델은 새로운 꽃과 측정값이 가까운 기존 꽃들의 품종을 참고하여 분류합니다.

```python
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# 특징(X)과 정답(y) 준비
iris = load_iris()
X = iris.data
y = iris.target

# 학습 데이터와 평가 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 모델 학습
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# 평가 데이터에 대한 예측과 정확도 계산
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.3f}")
```

**코드의 흐름**

1. `X`에는 꽃의 측정값, `y`에는 실제 품종을 저장합니다.
2. 데이터를 학습용과 평가용으로 나누어, 모델이 학습하지 않은 자료로 예측을 확인합니다.
3. `fit()`으로 학습한 뒤 `predict()`로 품종을 예측합니다. `n_neighbors=5`는 가까운 데이터 5개를 참고한다는 의미입니다.
4. `accuracy_score()`로 평가 데이터에서 정답을 맞힌 비율을 계산합니다.

**결과 해석:** 정확도가 높더라도 모든 종류의 꽃을 정확히 구분한다고 단정할 수는 없습니다. 이 예제는 제한된 데이터셋에서 학습과 평가 과정을 익히기 위한 것입니다. 모델의 일반화 성능과 평가 방법은 Chapter 04에서 자세히 다룹니다.

## Learning Materials

각 Chapter는 주제의 난이도에 따라 다음 내용을 포함합니다.

| 구성 | 학습 내용 |
|---|---|
| **Concepts** | 핵심 개념, 필요한 배경지식, 알고리즘의 작동 원리 |
| **Mathematical Foundations** | 필요한 수식, 기호 설명, 간단한 계산 예제와 Python 구현 |
| **Examples** | 단계별 실행 코드와 결과 해석 |
| **Coding Practice** | 직접 완성하는 연습문제, 코드 힌트와 해설 |
| **Mini Projects** | 배운 개념을 적용하는 소규모 프로젝트 |
| **Advanced Projects** | 여러 개념을 결합해 구현·검증하는 심화 프로젝트 |
| **Quiz & Summary** | 개념·코드 분석 문제, 접이식 정답·해설, 핵심 정리 |

어려운 수학적 유도나 추가 심화 학습은 필요한 경우 각 Chapter의 별도 `advanced/README.md`에서 다룹니다. 이해에 필요한 수식을 생략하지 않되, 복잡한 증명보다 개념·계산·코드의 관계를 우선 설명합니다.


## References

- [Google Colab](https://colab.research.google.com/)
- [Google Colab — FAQ](https://research.google.com/colaboratory/faq.html?hl=ko)

- [Python Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [scikit-learn — Getting Started](https://scikit-learn.org/stable/getting_started.html)
- [scikit-learn — User Guide](https://scikit-learn.org/stable/user_guide.html)
- [PyTorch — Get Started](https://pytorch.org/get-started/locally/)
- [PyTorch Documentation](https://docs.pytorch.org/docs/stable/index.html)
- [Hugging Face — Transformers](https://huggingface.co/docs/transformers/index)
- [Hugging Face — Datasets](https://huggingface.co/docs/datasets/index)
- [Hugging Face — PEFT](https://huggingface.co/docs/peft/index)

---

[← MoreStudy](../README.md) · [Data Processing](../Data_Processing/) · [Data Visualization](../Data_Visualization/)
