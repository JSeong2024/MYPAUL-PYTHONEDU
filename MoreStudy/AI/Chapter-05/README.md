[← AI 목차](../README.md#contents) · [Chapter 04](../Chapter-04/README.md)

# Chapter 05. PyTorch Fundamentals

PyTorch의 기본 데이터 구조인 Tensor부터 자동 미분(Autograd), Dataset과 DataLoader까지 학습합니다. NumPy로 계산하던 배열을 Tensor로 옮겨 보고, 계산 결과에 대한 Gradient를 구한 뒤 실제 CSV 데이터를 Mini-Batch로 처리하는 과정까지 연결합니다.

이번 Chapter의 목표는 신경망 이론을 미리 공부하는 것이 아닙니다. **PyTorch 코드의 입력 Shape를 읽고, 계산 결과를 확인하고, 데이터와 Gradient를 안전하게 다룰 수 있도록 익히는 것**이 핵심입니다. 신경망의 구조는 Chapter 06, 본격적인 Training Loop와 Optimizer는 Chapter 07에서 다룹니다.

- **기준 언어:** Python 3.11 이상 권장
- **주요 라이브러리:** PyTorch, NumPy, Pandas, Matplotlib
- **실행 환경:** Google Colab(기본), VS Code, Jupyter Notebook
- **선행 학습:** NumPy 배열 연산, 함수, 클래스 기초, Chapter 02의 Loss와 Gradient Descent
- **실습 규모:** 기본 예제와 모든 프로젝트를 CPU에서 실행 가능

## Contents

| Section | Topic |
|:---:|---|
| [5.1](#section-5-1) | **Learning Goals & Getting Started** — 실행 환경과 학습 목표 |
| [5.2](#section-5-2) | **Why PyTorch?** — NumPy, scikit-learn, PyTorch의 역할 |
| [5.3](#section-5-3) | **Creating Tensors** — 생성, Shape, Dtype, Device |
| [5.4](#section-5-4) | **Indexing, Reshape & Views** — 데이터 선택과 차원 변환 |
| [5.5](#section-5-5) | **Broadcasting** — Shape가 다른 Tensor 사이의 연산 |
| [5.6](#section-5-6) | **Tensor Operations** — Reduction, Matrix Multiplication |
| [5.7](#section-5-7) | **NumPy Interoperability** — 변환과 메모리 공유 |
| [5.8](#section-5-8) | **CPU/GPU & Device Management** — Device 이동과 주의사항 |
| [5.9](#section-5-9) | **Autograd & Computational Graph** — Chain Rule과 자동 미분 |
| [5.10](#section-5-10) | **Gradient Management** — 누적, 초기화, no_grad, detach |
| [5.11](#section-5-11) | **Dataset, DataLoader & Mini-Batch** — 데이터 공급 구조 |
| [5.12](#section-5-12) | **Examples & Coding Practice** — 실행 예제와 직접 구현 |
| [5.13](#section-5-13) | **Mini Projects** — 센서 Tensor 처리와 보정식 미분 |
| [5.14](#section-5-14) | **Advanced Projects** — Custom Dataset과 Gradient Audit |
| [5.15](#section-5-15) | **Quiz** — 개념, 코드 분석, 계산 문제 |
| [5.16](#section-5-16) | **Summary** — 핵심 내용 정리 |
| [5.17](#section-5-17) | **References** — 공식 문서 |

---

<a id="section-5-1"></a>
## 5.1. Learning Goals & Getting Started

### 학습 목표

이번 Chapter를 마치면 다음 작업을 할 수 있어야 합니다.

1. Tensor의 Shape·Dtype·Device를 확인하고 목적에 맞게 변환합니다.
2. Indexing·Broadcasting·Reduction·Matrix Multiplication을 구분해 적용합니다.
3. NumPy와 Tensor를 변환할 때 메모리 공유와 Device 제약을 판단합니다.
4. Autograd로 계산 그래프를 구성하고 `.backward()`로 Gradient를 확인합니다.
5. Gradient 누적과 초기화, `torch.no_grad()`와 `detach()`의 차이를 설명합니다.
6. TensorDataset 또는 Custom Dataset을 작성하고 DataLoader로 데이터를 Batch 단위로 가져옵니다.

### 실행 준비

Google Colab에서 다음 코드를 실행합니다. PyTorch가 이미 설치되어 있다면 설치 단계를 건너뜁니다.

```python
import torch
print('PyTorch:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
```

로컬에서는 `Chapter-05/` 폴더를 기준으로 필요한 패키지를 설치하고 예제를 실행합니다.

```bash
python -m pip install -r requirements.txt
python examples/01_tensor_basics.py
python -m unittest discover -s tests -v
```

PyTorch의 설치 명령은 운영체제와 가속기 환경에 따라 달라집니다. CUDA 등의 가속기 지원이 필요한 경우 [공식 설치 안내](https://pytorch.org/get-started/locally/)에서 환경에 맞는 명령을 선택합니다. **이 Chapter에서는 GPU가 없어도 모든 필수 코드를 실행할 수 있습니다.**

Google Colab에서는 프로젝트가 저장소에 게시된 뒤 저장소를 내려받아 실행할 수 있습니다. CSV를 사용하는 실습은 해당 Chapter 폴더를 함께 업로드해도 됩니다.

```python
# Colab 코드 셀 — GitHub에 배포된 뒤 사용
# !git clone --depth 1 https://github.com/JSeong2024/MYPAUL-PYTHONEDU.git
# %cd MYPAUL-PYTHONEDU/MoreStudy/AI/Chapter-05
```

### 실습 데이터

| 데이터셋 | 크기 | 용도 |
|---|---:|---|
| [`sensor_readings.csv`](./data/sensor_readings.csv) | 20일 × 센서 4개 | Broadcasting, Mask, Reduction |
| [`calibration_pairs.csv`](./data/calibration_pairs.csv) | 12행 | Autograd와 한 단계 Parameter 갱신 |
| [`facility_events.csv`](./data/facility_events.csv) | 48행 | Custom Dataset과 DataLoader |
| [`gradient_audit.csv`](./data/gradient_audit.csv) | 13행 | Autograd와 수치 Gradient 비교 |

네 데이터셋은 모두 **실습용 합성 데이터**입니다. 오류 입력 테스트용 `facility_events_invalid.csv`도 포함합니다. 열의 의미와 생성 방법은 [`data/README.md`](./data/README.md)에서 확인할 수 있습니다.

---

<a id="section-5-2"></a>
## 5.2. Why PyTorch?

### 머신러닝 라이브러리와의 관계

Chapter 01~04에서는 주로 scikit-learn을 사용했습니다. `fit()`과 `predict()`로 모델을 학습하고, 평가 지표와 검증 방식에 집중했습니다. PyTorch에서는 데이터를 Tensor로 표현하고 계산 과정을 직접 구성할 수 있으며, 연산 결과의 Gradient도 자동으로 얻을 수 있습니다.

| 도구 | 중심 역할 | 대표적인 사용 상황 |
|---|---|---|
| **NumPy** | 수치 배열·행렬 연산 | 데이터 계산, 배열 변환 |
| **Pandas** | 표 형태의 데이터 처리 | CSV 읽기, 열 선택, 결측값 검사 |
| **scikit-learn** | 전통적인 머신러닝 모델·평가 | Regression, Classification, Pipeline, Cross-Validation |
| **PyTorch** | Tensor 연산과 자동 미분, 신경망 구성 | Gradient가 필요한 사용자 정의 계산, 딥러닝 |

PyTorch는 scikit-learn의 단순한 대체재가 아닙니다. 실제로 데이터를 Pandas로 정리한 다음 Tensor로 변환하는 조합이 자연스럽고, 이미 해결된 문제를 무조건 PyTorch로 다시 작성할 필요도 없습니다.

### Tensor가 필요한 이유

**텐서(Tensor)** 는 여러 차원의 값을 담는 자료구조입니다. 하나의 값은 0차원, 숫자의 나열은 1차원, 행과 열로 구성된 표는 2차원 Tensor로 표현합니다. 이미지나 여러 장의 이미지처럼 더 많은 축이 필요하면 3차원 이상으로 확장합니다.

| Shape | 예시 | 해석 |
|---|---|---|
| `()` | `torch.tensor(3.0)` | Scalar, 0차원 |
| `(3,)` | `[10, 20, 30]` | Vector, 1차원 |
| `(2, 3)` | 두 Sample과 세 Feature | Matrix, 2차원 |
| `(8, 1, 28, 28)` | 이미지 8장, 채널 1개, 높이·너비 28 | 4차원 Batch |

Shape는 데이터가 몇 개 있는지만 알려주지 않습니다. **각 축이 무엇을 의미하는지**까지 이해해야 연산 오류를 피할 수 있습니다.

---

<a id="section-5-3"></a>
## 5.3. Creating Tensors

### Tensor 생성

```python
import torch

prices = torch.tensor([1200, 2400, 1800])
readings = torch.tensor([[10.0, 11.0], [12.0, 13.0]], dtype=torch.float32)
zeros = torch.zeros((2, 3))
ones = torch.ones((2, 3))
sequence = torch.arange(0, 6, dtype=torch.float32)

print(prices.dtype)          # torch.int64 (일반적인 정수 리스트)
print(readings.shape)        # torch.Size([2, 2])
print(zeros.shape)           # torch.Size([2, 3])
print(sequence)              # tensor([0., 1., 2., 3., 4., 5.])
```

주요 생성 함수는 다음과 같습니다.

| 함수 | 기능 | 참고 |
|---|---|---|
| `torch.tensor(data)` | 입력 데이터로 새 Tensor 생성 | 일반적으로 입력을 복사 |
| `torch.zeros(shape)` | 0으로 채운 Tensor | Shape를 튜플로 전달 가능 |
| `torch.ones(shape)` | 1로 채운 Tensor | 기본 실수 Dtype 사용 |
| `torch.arange(start, end, step)` | 일정 간격의 값 | 끝값 `end`는 포함하지 않음 |
| `torch.rand(shape)` | 0 이상 1 미만 균등 난수 | 결과 재현 시 Seed 고려 |
| `torch.randn(shape)` | 표준정규분포 난수 | 실험용 초기값에 자주 사용 |

무작위 값이 필요한 실습에서는 `torch.manual_seed(42)`로 PyTorch 난수 생성기의 상태를 설정할 수 있습니다. 다만 Seed를 고정하더라도 장치·연산·라이브러리 버전이 다르면 모든 결과가 비트 단위로 동일하게 재현된다고 보장할 수는 없습니다.

### Shape, Dtype, Device

모든 Tensor에서 특히 자주 확인하는 속성은 다음 세 가지입니다.

```python
x = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
print(x.shape)    # torch.Size([2, 3])
print(x.dtype)    # torch.float32
print(x.device)   # cpu (별도로 지정하지 않은 경우)
print(x.ndim)     # 2
print(x.numel())  # 6
```

- **Shape**: 각 축의 길이입니다. `(2, 3)`은 2행 3열로 이해할 수 있습니다.
- **Dtype**: 각 값의 저장 형식입니다. 계산에는 `float32`, Label에는 `int64`가 자주 사용됩니다.
- **Device**: 값이 저장된 계산 장치입니다. CPU 또는 지원되는 Accelerator가 해당합니다.

Dtype을 변경할 때는 `x.to(dtype=torch.float32)` 또는 `x.float()`를 사용합니다. 예를 들어 실수 평균이 필요하면 먼저 실수 Tensor로 변환하는 편이 명확합니다.

```python
counts = torch.tensor([1, 2, 3])
mean_value = counts.to(torch.float32).mean()
print(mean_value.item())  # 2.0
```

**중요:** Dtype을 바꿀 때 소수점이 잘릴 수 있고, `float32`에는 큰 정수를 정확하게 표현하는 데 한계가 있습니다. 단위나 데이터 범위를 검토한 후 변환합니다.

---

<a id="section-5-4"></a>
## 5.4. Indexing, Reshape & Views

### Indexing과 Slicing

다음 Tensor는 3일 동안 센서 2개가 측정한 기록입니다.

```python
values = torch.tensor([
    [18., 21.],
    [20., 23.],
    [19., 25.],
])

print(values[0])       # 첫날 기록: [18., 21.]
print(values[:, 1])    # 두 번째 센서: [21., 23., 25.]
print(values[1:, :])   # 두 번째 날부터 모든 센서
print(values[values[:, 0] >= 19])  # 첫 번째 센서가 19 이상인 행
```

일반적인 Slicing은 원본 Tensor의 메모리를 공유하는 View를 만들 수 있습니다. 반면 Boolean Indexing처럼 조건에 따라 선택하면 보통 새로운 Tensor가 만들어집니다. 따라서 원본 데이터를 수정할 의도가 없다면 가공할 결과에 `.clone()`을 사용하는 방법도 고려합니다.

### Reshape와 차원 추가

```python
x = torch.arange(12, dtype=torch.float32)
matrix = x.reshape(3, 4)
print(matrix.shape)             # [3, 4]
print(matrix.unsqueeze(0).shape) # [1, 3, 4]
print(matrix.squeeze().shape)    # [3, 4]
```

`reshape()`는 전체 원소 수를 유지하면서 Shape를 바꿉니다. 새 Shape의 원소 수가 원래와 다르면 오류가 발생합니다. `reshape()`가 반환하는 Tensor는 View일 수도, 복사본일 수도 있으므로 반드시 독립적인 저장 공간이 필요하면 `.clone()`을 사용합니다.

`unsqueeze(dim)`은 크기가 1인 축을 추가하고, `squeeze(dim)`은 지정한 크기 1의 축을 제거합니다. `squeeze()`를 인수 없이 사용하면 **모든 크기 1의 축이 제거**되므로 Batch 크기가 1일 때 의도치 않게 차원이 사라질 수 있습니다.

---

<a id="section-5-5"></a>
## 5.5. Broadcasting

**브로드캐스팅(Broadcasting)** 은 Shape가 서로 달라도 규칙을 만족하면 연산을 수행할 수 있도록 크기를 맞추는 방식입니다. 별도로 Tensor를 반복 복사하지 않고도 각 열에 서로 다른 보정값을 적용할 수 있습니다.

```python
readings = torch.tensor([
    [10., 20., 30.],
    [11., 21., 31.],
])
offsets = torch.tensor([1., -2., 3.])
print(readings + offsets)
# tensor([[11., 18., 33.],
#         [12., 19., 34.]])
```

`readings`의 Shape는 `(2,3)`, `offsets`는 `(3,)`입니다. 마지막 축부터 비교했을 때 차원 크기가 같거나 둘 중 하나가 1이면 Broadcast가 가능합니다. 축 수가 부족한 쪽은 앞에 크기 1의 축이 있는 것처럼 취급됩니다.

| 첫 번째 Shape | 두 번째 Shape | 결과 | 이유 |
|---|---|---|---|
| `(2, 3)` | `(3,)` | `(2, 3)` | 열 단위로 확장 |
| `(2, 3)` | `(2, 1)` | `(2, 3)` | 행 단위로 확장 |
| `(4, 1, 3)` | `(2, 3)` | `(4, 2, 3)` | 끝에서부터 각 축이 호환 |
| `(2, 3)` | `(2,)` | 오류 | 마지막 축 3과 2가 호환되지 않음 |

### Mask와 결측값

```python
samples = torch.tensor([[12., -1., 19.], [14., 15., -1.]])
valid = samples >= 0
filtered = torch.where(valid, samples, torch.zeros_like(samples))
counts = valid.sum(dim=0)
averages = filtered.sum(dim=0) / counts
print(counts.tolist())   # [2, 1, 1]
print(averages.tolist()) # [13.0, 15.0, 19.0]
```

여기에서 `-1`은 측정 실패를 뜻하는 **데이터 규칙**입니다. 이를 잘못된 값으로 간주한다는 조건이 명확해야 Mask를 적용할 수 있습니다. 정상 측정값이 음수일 수 있는 데이터라면 `samples >= 0`을 무조건 사용하면 안 됩니다. 모든 값이 결측인 열에서는 `counts == 0`이 발생하므로 이를 먼저 검사해야 합니다.

---

<a id="section-5-6"></a>
## 5.6. Tensor Operations

### 원소별 연산과 Reduction

`+`, `-`, `*`, `/`는 기본적으로 원소별 연산입니다. 반면 **축 방향 집계(Reduction)** 는 특정 축의 값을 묶어 합계·평균·최댓값 등을 계산합니다.

```python
x = torch.tensor([[2., 4., 6.], [8., 10., 12.]])
print((x * 2).tolist())             # 각 원소를 두 배
print(x.sum().item())              # 42.0
print(x.mean(dim=0).tolist())      # [5.0, 7.0, 9.0] — 열별 평균
print(x.mean(dim=1).tolist())      # [4.0, 10.0] — 행별 평균
print(x.mean(dim=1, keepdim=True).shape) # [2, 1]
```

여기서 `dim=0`은 0번 축(행 방향)을 줄여 열별 결과를 얻는다는 의미입니다. `keepdim=True`로 집계 후에도 해당 축을 길이 1로 유지할 수 있어 후속 Broadcasting에 유용합니다.

### Matrix Multiplication

`*`는 원소별 곱셈이고 `@` 또는 `torch.matmul()`은 행렬 곱셈입니다.

$$
C_{ij}=\sum_{k=1}^{p}A_{ik}B_{kj}
$$

- $A$: Shape $(m,p)$인 행렬
- $B$: Shape $(p,n)$인 행렬
- $C$: Shape $(m,n)$인 결과 행렬

```python
features = torch.tensor([[1., 2.], [3., 4.]]) # [2, 2]
weights = torch.tensor([[10.], [100.]])        # [2, 1]
predictions = features @ weights
print(predictions.tolist())   # [[210.0], [430.0]]
print(predictions.shape)      # torch.Size([2, 1])
```

첫 번째 Sample에서는 $1\times10+2\times100=210$입니다. 두 번째 Sample에서는 $3\times10+4\times100=430$입니다. 행렬 곱에서 안쪽 차원 $(p)$이 같아야 한다는 점이 핵심입니다.

---

<a id="section-5-7"></a>
## 5.7. NumPy Interoperability

NumPy 배열을 PyTorch Tensor로 옮기는 방법에는 서로 다른 메모리 동작이 있습니다.

```python
import numpy as np
import torch

source = np.array([1., 2., 3.], dtype=np.float32)
a = torch.from_numpy(source)
b = torch.tensor(source)

source[0] = 99.
print(a[0].item())  # 99.0 — 같은 메모리 공유
print(b[0].item())  # 1.0  — 별도의 Tensor
```

| 코드 | 일반적인 동작 | 주의 |
|---|---|---|
| `torch.tensor(array)` | 값을 복사하여 새 Tensor 생성 | 원본 배열 변경의 영향을 받지 않음 |
| `torch.from_numpy(array)` | NumPy 배열과 CPU 메모리 공유 | 한쪽의 값 변경이 다른 쪽에 반영될 수 있음 |
| `torch.as_tensor(array)` | 가능한 경우 복사를 피함 | 입력 형식에 따라 공유 여부가 달라짐 |
| `tensor.numpy()` | CPU Tensor를 NumPy 배열로 변환 | Gradient 추적과 장치 조건 확인 필요 |

Gradient를 계산하고 있거나 GPU를 사용하는 Tensor의 결과를 NumPy로 확인할 때는 일반적으로 다음 방법을 사용합니다.

```python
x = torch.tensor([1., 2., 3.], requires_grad=True)
result = (x * 2).detach().cpu().numpy()
print(result)
```

`.detach()`는 계산 그래프와의 미분 연결을 끊고, `.cpu()`는 NumPy가 다룰 수 있도록 CPU 메모리로 옮깁니다. 이 결과가 저장 공간을 공유할 수 있으므로 독립적인 NumPy 복사본이 필요한 경우에는 `.copy()`를 추가합니다. `.detach()`로 생성한 Tensor도 원본과 메모리를 공유할 수 있다는 점을 기억하세요.

---

<a id="section-5-8"></a>
## 5.8. CPU/GPU & Device Management

GPU는 병렬 연산에 유리하지만 작은 Tensor 연산에서는 데이터 이동 비용 때문에 CPU보다 빠르다는 보장이 없습니다. 이 Chapter에서는 CPU를 기본으로 사용합니다.

```python
import torch

def select_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return torch.device('mps')
    return torch.device('cpu')

device = select_device()
x = torch.tensor([1., 2., 3.]).to(device)
y = torch.ones(3, device=device)
print('device:', device)
print('result:', (x + y).detach().cpu().tolist())
```

`torch.cuda.is_available()`은 CUDA 사용 가능 여부를 확인합니다. Apple Silicon을 사용하는 macOS에서는 지원 환경에 따라 `mps`를 선택할 수 있습니다. 특정 GPU가 없으면 CPU로 진행하면 됩니다.

### Device와 Dtype 불일치

같은 연산에 사용하는 Tensor가 서로 다른 장치에 있으면 오류가 발생할 수 있습니다. 한쪽만 GPU로 옮기고 다른 쪽을 CPU에 남겨두지 않도록 합니다.

```python
batch = torch.ones((4, 3))
weights = torch.tensor([0.2, 0.3, 0.5])
batch = batch.to(device)
weights = weights.to(device=device, dtype=batch.dtype)
result = batch @ weights
```

`to()`는 목적 장치·형식이 이미 같으면 원래 Tensor를 그대로 반환할 수도 있고, 이동·변환이 필요하면 새로운 Tensor를 반환합니다. 따라서 `x.to(device)`만 호출하고 반환값을 버리면 원본 변수가 다른 Device를 가리킬 수 있습니다. `x = x.to(device)`처럼 결과를 받습니다.

### CPU에서 결과 확인

```python
scalar = result.mean()
print(scalar.detach().cpu().item())
```

`.item()`은 원소가 하나인 Tensor만 Python 숫자로 바꿉니다. 반복문 안에서 GPU Tensor에 `.item()`을 자주 호출하면 동기화 비용이 생길 수 있으므로, 큰 작업에서는 필요한 시점에만 결과를 꺼내는 편이 좋습니다.

---

<a id="section-5-9"></a>
## 5.9. Autograd & Computational Graph

### 자동 미분의 역할

**자동 미분(Automatic Differentiation, Autograd)** 은 Tensor 계산에 사용된 연산을 기록하고, 결과를 입력값으로 미분하는 기능입니다. Chapter 02에서는 MSE의 Gradient를 직접 계산했지만, PyTorch에서는 계산식을 Tensor 연산으로 작성하고 `.backward()`를 호출해 Gradient를 구할 수 있습니다.

계산 그래프(Computational Graph)는 어떤 Tensor가 어떤 연산을 거쳐 만들어졌는지 나타내는 관계입니다. PyTorch는 연산을 실행할 때 동적으로 그래프를 구성합니다.

예를 들어 다음 계산을 생각해 봅니다.

$$
z=wx+b,\qquad L=z^2
$$

여기서 $w=2$, $x=3$, $b=1$이면 $z=7$, $L=49$입니다. Chain Rule에 따르면 다음과 같습니다.

$$
\frac{\partial L}{\partial w}=
\frac{\partial L}{\partial z}\cdot\frac{\partial z}{\partial w}
=2z\cdot x=2\times7\times3=42
$$

$$
\frac{\partial L}{\partial b}=2z\cdot1=14
$$

Tensor에서는 같은 계산을 다음처럼 작성합니다.

```python
import torch

x = torch.tensor(3.0)
w = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)
z = w * x + b
loss = z.square()
loss.backward()

print(loss.item()) # 49.0
print(w.grad.item()) # 42.0
print(b.grad.item()) # 14.0
```

`requires_grad=True`인 Leaf Tensor `w`, `b`에 대해 `.grad`가 계산됩니다. `z`와 `loss`처럼 연산 결과로 생성된 Tensor는 `grad_fn`을 통해 그래프의 연결을 확인할 수 있습니다. 일반적으로 중간 Tensor의 `.grad`는 자동으로 보존되지 않습니다.

### Scalar Loss와 backward

여러 Sample의 손실을 모아 미분할 때에는 보통 `mean()`이나 `sum()`으로 **스칼라 Loss**를 만듭니다.

```python
x = torch.tensor([1., 2., 3.])
w = torch.tensor(1.0, requires_grad=True)
errors = (w * x - 2 * x).square() # Shape [3]
loss = errors.mean()             # Shape []
loss.backward()
print(w.grad.item())             # 음수: w를 늘리면 Loss가 감소하는 방향
```

`errors.backward()`처럼 여러 원소가 있는 Tensor에서 Gradient의 방향을 지정하지 않으면 오류가 발생합니다. 여러 출력의 Gradient가 필요한 경우에는 별도의 Gradient 인수를 전달할 수 있지만, 이번 과정에서는 스칼라 Loss를 기준으로 이해하면 충분합니다.

---

<a id="section-5-10"></a>
## 5.10. Gradient Management

### Gradient는 자동으로 누적됩니다

PyTorch의 `.backward()`는 기존 `.grad` 값을 덮어쓰기보다는 **Gradient를 누적**합니다.

```python
w = torch.tensor(2.0, requires_grad=True)
(w * 3).backward()
print(w.grad.item()) # 3.0
(w * 3).backward()    # 새 계산 그래프를 사용
print(w.grad.item()) # 6.0
w.grad = None        # 누적 Gradient 초기화
```

두 번의 계산이 의도한 누적이 아니라면 다음 Gradient 계산 전에 `.grad`를 초기화해야 합니다. `w.grad.zero_()`처럼 기존 Gradient Tensor를 0으로 만드는 방식도 사용할 수 있지만, `.grad`가 아직 `None`이면 `zero_()`를 호출할 수 없습니다.

### no_grad와 detach

| 기능 | 의미 | 주된 상황 |
|---|---|---|
| `torch.no_grad()` | 블록 안에서 새 연산의 Gradient 추적을 끔 | Parameter 값을 직접 갱신, 결과 계산 |
| `tensor.detach()` | 특정 Tensor를 그래프에서 분리 | 결과 기록, NumPy 변환 |
| `torch.inference_mode()` | 추론 전용으로 추가적인 추적 비용을 줄임 | Gradient가 필요 없는 순수 추론 경로 |

```python
w = torch.tensor(2.0, requires_grad=True)
with torch.no_grad():
    w -= 0.1
print(w.item())  # 1.9
```

`inference_mode()`에서 만든 Tensor에는 Autograd와 관련한 제약이 추가로 적용되므로, 이후 Gradient를 계산할 값까지 무조건 그 안에서 만들지는 않습니다. 기본 실습에서는 `no_grad()`를 우선 사용합니다.

### 한 번의 Parameter 갱신

학습률(Learning Rate) $\eta$는 Gradient를 따라 Parameter를 어느 정도 변경할지 결정하는 값입니다.

$$
\theta_{\mathrm{new}}=\theta-\eta\nabla_\theta L
$$

Chapter 02와 동일한 갱신식입니다. PyTorch는 $\nabla_\theta L$을 계산하는 부분을 자동화합니다.

```python
w = torch.tensor(1.0, requires_grad=True)
x, target = torch.tensor(2.0), torch.tensor(6.0)
loss = (w * x - target).square() # (2 - 6)^2 = 16
loss.backward()                 # dL/dw = 2(2-6)*2 = -16
with torch.no_grad():
    w -= 0.1 * w.grad            # w = 1 - 0.1*(-16) = 2.6
w.grad = None
print(w.item())                  # 약 2.6
```

이 코드는 한 번의 업데이트를 보여 줍니다. 여러 데이터 Batch와 Optimizer를 연결하는 전체 학습 구조는 Chapter 07에서 다룹니다.

### In-place 연산 주의

메서드 이름이 `_`로 끝나는 `add_()`, `mul_()` 등은 원본 값을 직접 변경하는 In-place 연산입니다. Autograd가 미분에 필요한 기존 값을 기억하고 있을 때 원본을 수정하면 오류가 발생할 수 있습니다. Gradient가 걸린 Leaf Tensor를 직접 변경하는 연산은 `torch.no_grad()` 안에서 사용하도록 합니다.

---

<a id="section-5-11"></a>
## 5.11. Dataset, DataLoader & Mini-Batch

### Dataset은 무엇을 제공하나요?

실습 데이터가 작은 경우에는 모든 Sample을 한 번에 Tensor로 만들 수 있습니다. 그러나 실제 학습에서는 입력과 Target을 짝지어 유지하면서 일정한 크기만큼 나눠 처리하는 편이 유용합니다.

**데이터셋(Dataset)** 은 개별 Sample을 가져오는 규칙을 제공하고, **데이터 로더(DataLoader)** 는 Dataset에서 Sample을 읽어 Batch 단위로 묶어 전달하는 도구입니다.

```python
import torch
from torch.utils.data import TensorDataset, DataLoader

X = torch.tensor([[1., 2.], [3., 4.], [5., 6.], [7., 8.], [9., 10.]])
y = torch.tensor([0, 1, 1, 0, 1], dtype=torch.int64)
dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=2, shuffle=False)

for features, labels in loader:
    print(features.shape, labels.shape)
# [2,2] [2]
# [2,2] [2]
# [1,2] [1]
```

여기서 **미니배치(Mini-Batch)** 는 전체 데이터보다 작은 묶음을 뜻합니다. `batch_size=2`이면 Sample 5개가 2개, 2개, 1개씩 묶입니다. 마지막 Batch의 크기는 반드시 `batch_size`와 같지 않습니다.

| DataLoader 매개변수 | 기능 |
|---|---|
| `batch_size` | 한 번에 꺼낼 Sample 수 |
| `shuffle` | 순회 순서를 섞을지 여부 |
| `drop_last` | 마지막 불완전 Batch를 제외할지 여부 |
| `num_workers` | 병렬 데이터 로딩 프로세스 수, `0`은 메인 프로세스 로딩 |
| `generator` | Shuffle 등의 난수 생성기 설정에 사용 가능 |

학습에는 `shuffle=True`가 유용할 때가 많지만, 시간 순서나 ID 순서를 보존해야 하는 평가·출력에는 `shuffle=False`가 적합할 수 있습니다. 시계열 데이터의 시간 순서를 섞어 학습·평가에 누출을 만들지 않도록 목적을 먼저 판단합니다.

### Custom Dataset 작성

기존 CSV를 처리하려면 `Dataset`을 상속받아 세 메서드를 구현합니다.

```python
from torch.utils.data import Dataset

class ReadingDataset(Dataset):
    def __init__(self, features, labels):
        if len(features) != len(labels):
            raise ValueError('Mismatched sample count')
        self.features = torch.as_tensor(features, dtype=torch.float32)
        self.labels = torch.as_tensor(labels, dtype=torch.int64)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return self.features[index], self.labels[index]
```

- `__init__`: 데이터 보관과 초기 검증
- `__len__`: Dataset의 Sample 수
- `__getitem__`: 특정 인덱스의 Sample 반환

예제는 메모리에 있는 Feature를 다루지만, 실제 프로젝트에서는 CSV 경로 또는 이미지 경로를 저장해 필요한 시점에 데이터를 읽을 수도 있습니다. Custom Dataset에서는 반환 순서와 Dtype을 일관되게 유지해야 DataLoader의 기본 묶음 동작을 활용할 수 있습니다.

### GPU와 배치 이동

DataLoader에서 데이터를 CPU Tensor로 받은 뒤 필요한 Batch만 Device로 이동하는 방식이 일반적입니다.

```python
for features, labels in loader:
    features = features.to(device)
    labels = labels.to(device)
    # 이후 Tensor 계산 수행
```

이번 Chapter에서는 대규모 DataLoader 최적화나 분산 학습을 다루지 않습니다. `num_workers=0`을 기본으로 두어 Colab과 Windows 환경에서 실행 차이를 줄입니다.

---

<a id="section-5-12"></a>
## 5.12. Examples & Coding Practice

### 실행 예제

| 예제 | 핵심 내용 | 실행 파일 |
|---|---|---|
| Example 01 | Tensor 생성·Shape·Dtype·NumPy 연동 | [`01_tensor_basics.py`](./examples/01_tensor_basics.py) |
| Example 02 | Broadcasting·Reduction·Matrix Multiplication | [`02_broadcasting_matrix.py`](./examples/02_broadcasting_matrix.py) |
| Example 03 | CPU/GPU Device 선택과 NumPy 변환 | [`03_device_numpy.py`](./examples/03_device_numpy.py) |
| Example 04 | Autograd와 Gradient 누적 | [`04_autograd.py`](./examples/04_autograd.py) |
| Example 05 | TensorDataset과 DataLoader | [`05_dataloader.py`](./examples/05_dataloader.py) |

```bash
python examples/01_tensor_basics.py
python examples/02_broadcasting_matrix.py
python examples/03_device_numpy.py
python examples/04_autograd.py
python examples/05_dataloader.py
```

실습용 Notebook [`Chapter_05_PyTorch_Fundamentals.ipynb`](./notebooks/Chapter_05_PyTorch_Fundamentals.ipynb)에서는 같은 개념을 한 셀씩 실행할 수 있습니다. Notebook은 외부 데이터 다운로드 없이 실행되는 코드와 짧은 설명으로 구성했습니다. 프로젝트 전체의 요구사항과 실행 방법은 각 프로젝트 README에서 확인합니다.

### Coding Practice

**Practice 01 — Tensor Shapes**

입력 Shape `[N,3]`인 Tensor의 열별 평균을 `float32` Shape `[3]`으로 반환합니다. `N=0`이거나 열 개수가 3이 아니면 오류로 처리합니다.

- 학생용: [`exercises/01_tensor_shapes.py`](./exercises/01_tensor_shapes.py)
- 모범답안: [`solutions/practice_01_tensor_shapes.py`](./solutions/practice_01_tensor_shapes.py)

**Practice 02 — Broadcasting & Mask**

`readings` Shape `[N,3]`, `offsets` Shape `[3]`을 입력받아 보정 결과와 원본 유효값(0 이상) Mask를 반환합니다. 유효하지 않은 원소도 보정 계산값에는 남을 수 있으므로, 후속 집계에서는 반드시 Mask를 사용합니다.

- 학생용: [`exercises/02_broadcast_mask.py`](./exercises/02_broadcast_mask.py)
- 모범답안: [`solutions/practice_02_broadcast_mask.py`](./solutions/practice_02_broadcast_mask.py)

**Practice 03 — Autograd Derivative**

$f(x)=3x^2+2x$의 Gradient를 임의의 입력 $x$에서 Autograd로 계산합니다. $x=2$이면 $f'(x)=6x+2=14$입니다.

- 학생용: [`exercises/03_autograd_derivative.py`](./exercises/03_autograd_derivative.py)
- 모범답안: [`solutions/practice_03_autograd_derivative.py`](./solutions/practice_03_autograd_derivative.py)

**Practice 04 — Batch Iteration**

`count`개의 Sample을 `batch_size`로 나누었을 때 Batch별 실제 크기를 리스트로 반환합니다. 예를 들어 10개를 4개씩 나누면 `[4,4,2]`입니다. `drop_last=False`를 사용합니다.

- 학생용: [`exercises/04_batch_iteration.py`](./exercises/04_batch_iteration.py)
- 모범답안: [`solutions/practice_04_batch_iteration.py`](./solutions/practice_04_batch_iteration.py)

<details>
<summary><strong>Practice 정답 확인 방법</strong></summary>

모범 구현을 직접 실행하거나 자동 테스트로 확인합니다.

```bash
python solutions/practice_01_tensor_shapes.py
python solutions/practice_02_broadcast_mask.py
python solutions/practice_03_autograd_derivative.py
python solutions/practice_04_batch_iteration.py
python -m unittest discover -s tests -v
```

학생용 함수는 `NotImplementedError`를 사용해 미완성 상태를 나타냅니다. 모범답안과 같은 입력·출력 규격으로 완성한 뒤 테스트합니다.

</details>

---

<a id="section-5-13"></a>
## 5.13. Mini Projects

Mini Project에서는 Tensor 연산과 Autograd를 독립적인 작업에 적용합니다. 신경망이나 대규모 Dataset은 필요하지 않습니다.

| 프로젝트 | 학습 내용 | 자료 |
|---|---|---|
| **Mini 01 — Sensor Tensor Quality Report** | 센서 보정, 유효값 Mask, 열별 집계, CSV 출력 | [프로젝트 README](./projects/mini_01_sensor_tensors/README.md) · [결과 그림](./figures/mini_01_sensor_counts.png) |
| **Mini 02 — Autograd Calibration** | MSE Gradient, Parameter 한 번 갱신, Loss 변화 확인 | [프로젝트 README](./projects/mini_02_autograd_calibration/README.md) · [결과 그림](./figures/mini_02_calibration_step.png) |

Mini 01의 기본 데이터에서는 `sensor_02`, `sensor_04`에 각각 2개의 결측 측정이 존재합니다. Mini 02의 기본 데이터에서는 Learning Rate 0.03으로 한 단계 업데이트했을 때 Loss가 약 `33.2871`에서 `3.4890`으로 감소합니다. **한 번의 업데이트에서 Loss가 감소했다고 해서 모든 데이터와 Learning Rate에서 항상 감소하는 것은 아닙니다.**

---

<a id="section-5-14"></a>
## 5.14. Advanced Projects

Advanced Project에서는 동작하는 코드뿐 아니라 데이터 검증과 수치 결과의 신뢰성을 확인합니다.

| 프로젝트 | 학습 내용 | 자료 |
|---|---|---|
| **Advanced 01 — Facility Event Data Pipeline** | Custom Dataset, DataLoader, 배치 집계, 원본 ID 보존 | [프로젝트 README](./projects/advanced_01_custom_dataloader/README.md) · [결과 그림](./figures/advanced_01_batch_sizes.png) |
| **Advanced 02 — Gradient Audit & Numerical Check** | Autograd와 중심 차분 비교, 오차 검증, Gradient 추적 점검 | [프로젝트 README](./projects/advanced_02_gradient_audit/README.md) · [결과 그림](./figures/advanced_02_gradient_comparison.png) |

Advanced 01은 CSV의 유효성을 검사하고 Batch 단위 처리 결과가 전체 Sample을 빠짐없이 포함하는지 확인합니다. Advanced 02는 Gradient 값이 정확한지 **수치 계산과 비교하는 검증 절차**를 익히는 데 목적이 있습니다.

### 프로젝트 실행

```bash
python solutions/mini_01_sensor_tensors.py
python solutions/mini_02_autograd_calibration.py
python solutions/advanced_01_custom_dataloader.py
python solutions/advanced_02_gradient_audit.py
python -m unittest discover -s tests -v
```

모범 구현은 기본적으로 `outputs/` 아래에 CSV 결과를 저장합니다. 각 프로젝트의 입력 파일, 출력 형식, 코드 힌트, 검증 조건은 프로젝트 README에 별도로 정리했습니다.

---

<a id="section-5-15"></a>
## 5.15. Quiz — PyTorch Fundamentals

### 객관식

**Q-01.** NumPy 배열과 비교할 때 PyTorch Tensor의 주요 특징으로 가장 적절한 것은 무엇인가요?

1. 모든 Tensor는 GPU에서만 연산할 수 있습니다.
2. Tensor는 자동 미분과 하드웨어 Accelerator 연산을 지원할 수 있습니다.
3. Tensor는 정수값을 저장할 수 없습니다.
4. Tensor를 만들면 항상 `requires_grad=True`가 적용됩니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②** Tensor는 CPU에서도 사용할 수 있고 정수·실수 등 여러 Dtype을 지원합니다. Autograd는 필요한 Tensor에서 `requires_grad=True`를 설정해야 Gradient를 추적합니다.

</details>

**Q-02.** `x = torch.tensor([1, 2, 3])`일 때 `x.dtype`으로 가장 일반적인 값은 무엇인가요?

1. `torch.float32`
2. `torch.float64`
3. `torch.int64`
4. `torch.bool`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③** 일반적인 Python 정수 리스트에서 Dtype이 추론되므로 `torch.int64`가 됩니다. 실수 Tensor가 필요하면 `dtype=torch.float32` 등을 명시합니다.

</details>

**Q-03.** Shape가 `(5,3)`인 Tensor와 Broadcasting으로 직접 더할 수 없는 Shape는 무엇인가요?

1. `(3,)`
2. `(1,3)`
3. `(5,1)`
4. `(5,)`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ④** Broadcasting은 끝 축부터 비교합니다. `(5,3)`의 마지막 축 3과 `(5,)`의 마지막 축 5가 맞지 않으며 어느 쪽도 1이 아니므로 연산할 수 없습니다.

</details>

**Q-04.** `loss.backward()` 호출 후 Leaf Tensor의 `.grad`를 초기화하지 않고, 새 계산 그래프로 다시 `backward()`하면 어떻게 되나요?

1. 이전 Gradient를 삭제하고 새 값으로 교체합니다.
2. 기본적으로 Gradient가 기존 `.grad`에 더해집니다.
3. 자동으로 Parameter 값까지 업데이트됩니다.
4. 항상 동일한 계산 그래프 오류가 발생합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②** 기본적으로 Gradient가 누적됩니다. 동일한 그래프를 그대로 두 번 역전파하면 별도 오류가 발생할 수 있지만, 문제는 새 그래프를 사용한다고 명시했습니다. Parameter 갱신은 직접 작성하거나 Optimizer로 처리해야 합니다.

</details>

**Q-05.** Sample 10개를 `DataLoader(batch_size=4, drop_last=False)`로 순회하면 Batch 크기는 어떤 순서인가요?

1. `[4, 4]`
2. `[4, 4, 4]`
3. `[4, 4, 2]`
4. `[10]`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③** 10개를 4개씩 묶으면 4개짜리 Batch 2개와 남은 2개짜리 Batch 1개가 생성됩니다. `drop_last=True`였다면 마지막 2개짜리 Batch는 제외됩니다.

</details>

**Q-06.** GPU에서 계산한 Tensor의 값을 NumPy 배열로 확인할 때 적절한 코드는 무엇인가요?

1. `tensor.numpy()`
2. `tensor.detach().cpu().numpy()`
3. `tensor.cuda().numpy()`
4. `tensor.item()`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②** 일반적으로 Gradient 추적을 끊고 CPU로 이동한 뒤 NumPy로 변환합니다. `.item()`은 단일 원소 Tensor에만 사용할 수 있습니다.

</details>

### 주관식 및 코드 분석

**Q-07.** 다음 코드의 출력 Shape와 값은 무엇인가요?

```python
import torch
x = torch.arange(12).reshape(3, 4)
print(x[:, 1].tolist())
print(x.float().mean(dim=0))
```

<details>
<summary><strong>정답 및 해설</strong></summary>

첫 번째 출력은 `[1, 5, 9]`입니다. 두 번째 출력은 `tensor([4., 5., 6., 7.])`이고 Shape는 `(4,)`입니다. `dim=0`은 행 축을 줄여 같은 열끼리 평균을 계산합니다. 원본 `x`는 정수 Tensor이므로 `.float()`로 변환한 뒤 평균을 구합니다.

</details>

**Q-08.** Shape가 `(6,4)`인 `X`와 `(4,2)`인 `W`에 대해 `X @ W`의 결과 Shape를 쓰고 그 이유를 설명하세요.

<details>
<summary><strong>정답 및 해설</strong></summary>

결과 Shape는 `(6,2)`입니다. 행렬 곱에서 왼쪽 행렬의 열 개수 4와 오른쪽 행렬의 행 개수 4가 같으므로 곱셈이 가능하고, 바깥쪽 축 6과 2가 결과 Shape에 남습니다.

</details>

**Q-09.** 다음 코드에서 `w.grad.item()` 값은 얼마인가요? 수식으로 계산해 보세요.

```python
w = torch.tensor(2.0, requires_grad=True)
x = torch.tensor(3.0)
loss = (w * x + 1).square()
loss.backward()
print(w.grad.item())
```

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: 42.0**. $L=(3w+1)^2$이고 미분하면 $dL/dw=2(3w+1)\times3$입니다. $w=2$를 대입하면 $2\times7\times3=42$입니다.

</details>

**Q-10.** 다음 코드에서 `x`와 `y`의 관계를 설명하세요. `y[0]`을 수정하면 `x[0]`도 바뀔 수 있나요?

```python
x = torch.tensor([1., 2., 3.])
y = x.detach()
```

<details>
<summary><strong>정답 및 해설</strong></summary>

바뀔 수 있습니다. `detach()`는 미분 그래프의 연결을 끊지만 새 Tensor가 원본과 저장 공간을 공유할 수 있기 때문입니다. 데이터의 독립적인 복사본이 필요하면 `x.detach().clone()`을 사용합니다.

</details>

**Q-11.** Custom Dataset에 `__len__`과 `__getitem__`이 필요한 이유를 설명하고, Label의 값이 `0` 또는 `1`이어야 하는 데이터에서 어떤 유효성 검사를 해야 하는지 작성하세요.

<details>
<summary><strong>정답 및 해설</strong></summary>

`__len__`은 Dataset 크기를 알려주고 `__getitem__`은 인덱스에 해당하는 Sample을 반환합니다. Dataset 생성 시 필수 열, 입력과 Label의 길이, 결측값, 숫자 변환 여부, Label이 0 또는 1인지 검사해야 합니다. `NaN`, `2`, `-1` 같은 값이 Label로 전달되지 않도록 처리합니다.

</details>

**Q-12.** 다음 코드의 두 번째 행에서 어떤 문제가 발생할 수 있는지 설명하고, 일반적인 수정 코드를 작성하세요.

```python
x = torch.tensor([1., 2., 3.], requires_grad=True)
array = (x * 2).numpy()
```

<details>
<summary><strong>정답 및 해설</strong></summary>

`x * 2`가 Autograd의 추적 대상이므로 그대로 `.numpy()`를 호출하면 오류가 발생합니다. CPU Tensor라면 `(x * 2).detach().numpy()`로 변환할 수 있으며, 장치와 관계없이 사용하는 코드는 `(x * 2).detach().cpu().numpy()`입니다.

</details>

---

<a id="section-5-16"></a>
## 5.16. Summary

- PyTorch Tensor는 Shape·Dtype·Device가 정해진 다차원 데이터 구조입니다.
- Indexing과 Reshape로 데이터를 선택·변환하고, Broadcasting과 Reduction으로 배열 전체를 효율적으로 계산합니다.
- `*`는 원소별 곱이고 `@`는 행렬 곱입니다. 연산 전에 Shape를 확인해야 합니다.
- NumPy와 Tensor는 메모리를 공유할 수 있습니다. 값 수정과 Gradient 추적의 차이를 구분합니다.
- CPU·GPU Device 이동에는 `.to(device)`를 사용하고, 반환값을 적절히 보관합니다.
- Autograd는 계산 그래프를 통해 Gradient를 구합니다. `.backward()` 후 Leaf Tensor의 `.grad`를 확인합니다.
- Gradient는 기본적으로 누적됩니다. 새 계산 전에 초기화하고, 직접 Parameter를 갱신할 때는 `torch.no_grad()`를 사용합니다.
- Dataset은 Sample을 제공하고 DataLoader는 Sample을 Batch로 묶습니다. 마지막 Batch 크기와 순회 순서를 확인해야 합니다.

### 실행 및 테스트

```bash
python scripts/make_datasets.py
python -m unittest discover -s tests -v
```

데이터를 다시 생성할 때는 기존 `data/` CSV를 덮어씁니다. 고정 Seed를 사용하므로 동일한 생성 스크립트와 버전에서 동일한 실습 입력을 만들도록 구성했습니다.

다음 Chapter에서는 이러한 Tensor와 Autograd를 이용해 신경망의 계층, 활성화 함수, Forward Pass와 Backpropagation의 구조를 학습합니다.

---

<a id="section-5-17"></a>
## 5.17. References

- [PyTorch — Start Locally](https://pytorch.org/get-started/locally/)
- [PyTorch — Tensors](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
- [PyTorch — Automatic Differentiation](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- [PyTorch — Datasets & DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
- [PyTorch — Tensor Attributes](https://docs.pytorch.org/docs/stable/tensor_attributes.html)
- [PyTorch — Autograd Mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)
- [PyTorch — Reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)
- [NumPy — The NumPy Array](https://numpy.org/doc/stable/reference/arrays.ndarray.html)

---

[← Chapter 04](../Chapter-04/README.md) · [← AI 목차](../README.md#contents)
