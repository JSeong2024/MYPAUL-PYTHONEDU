# Quiz & Review — Part 02

Chapter 05~07 · **객관식 16문항 · 주관식 8문항**

객관식은 가장 적절한 답을 하나 선택하십시오. 주관식은 계산 과정이나 판단 근거를 포함하여 답하십시오. 정답과 해설은 답안을 작성한 뒤 확인할 수 있습니다.

[← Summary 목차](./README.md) · [Problems](./problem.md) · [AI 목차](../README.md)

## 객관식

### Q-01.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

다음 코드의 실행 결과로 올바른 것은 무엇입니까?

```python
import torch

x = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
print(x.shape, x.dtype)
```

1. `torch.Size([3, 2]) torch.float32`
2. `torch.Size([2, 3]) torch.int64`
3. `torch.Size([2, 3]) torch.float32`
4. `torch.Size([6]) torch.float32`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

2행 3열의 2차원 텐서이므로 Shape는 `(2, 3)`입니다. `dtype=torch.float32`를 지정했으므로 정수 형태로 입력한 값도 `float32` 자료형으로 저장됩니다.

**오답 해설**

- **①:** 행과 열의 수를 뒤바꾸었습니다.
- **②:** `dtype`을 명시했으므로 `int64`가 아닙니다.
- **④:** 텐서를 1차원으로 펼치는 연산은 수행하지 않았습니다.

</details>

### Q-02.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

다음 중 PyTorch에서 두 텐서를 원소별로 더할 때 **Shape 오류 없이 실행되는 조합**은 무엇입니까?

1. `(4, 3)`과 `(4,)`
2. `(4, 3)`과 `(3,)`
3. `(4, 3)`과 `(2, 3)`
4. `(4, 3)`과 `(3, 4)`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

Broadcasting은 뒤쪽 차원부터 크기를 비교합니다. `(4, 3)`과 `(3,)`은 마지막 차원의 크기가 `3`으로 같으므로 두 번째 텐서가 각 행에 더해집니다. 결과 Shape는 `(4, 3)`입니다.

**오답 해설**

- **①:** 뒤쪽 차원 `3`과 `4`가 맞지 않습니다.
- **③:** 첫 차원 `4`와 `2`는 서로 다르고 어느 쪽도 `1`이 아닙니다.
- **④:** 마지막 차원부터 비교하면 `3`과 `4`가 일치하지 않습니다.

</details>

### Q-03.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

`A`의 Shape가 `(8, 5)`, `B`의 Shape가 `(5, 3)`일 때 `A @ B`의 결과 Shape는 무엇입니까?

1. `(8, 3)`
2. `(5, 5)`
3. `(8, 5, 3)`
4. `(3, 8)`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

행렬 곱에서는 왼쪽 행렬의 열 수와 오른쪽 행렬의 행 수가 같아야 합니다. 따라서 `(8, 5) @ (5, 3)`의 결과 Shape는 `(8, 3)`입니다.

</details>

### Q-04.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

CPU 메모리에 있는 NumPy 배열 `a`로 `x = torch.from_numpy(a)`를 실행했습니다. 이어서 `x[0] = 99`를 실행하면 어떻게 됩니까?

1. `torch.from_numpy()`는 항상 복사본을 만들므로 `a`는 변경되지 않습니다.
2. 일반적으로 저장 공간을 공유하므로 `a[0]`도 변경됩니다.
3. 텐서의 값을 변경하면 NumPy 배열의 Dtype이 자동으로 `float32`로 바뀝니다.
4. `torch.from_numpy()`는 GPU 배열만 입력받을 수 있습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

`torch.from_numpy()`로 만든 텐서는 NumPy 배열과 메모리를 공유합니다. 따라서 텐서에서 원소를 수정하면 원본 배열에도 반영됩니다. 독립적인 텐서가 필요하다면 `.clone()`을 사용할 수 있습니다. 단, 읽기 전용 배열이나 지원하지 않는 자료형은 별도로 주의해야 합니다.

**오답 해설**

- **①:** 항상 복사하는 함수가 아닙니다.
- **③:** 원소 값을 수정해도 배열의 Dtype은 바뀌지 않습니다.
- **④:** `torch.from_numpy()`는 NumPy 배열을 입력받는 함수로, GPU 배열만 허용하는 것이 아닙니다.

</details>

### Q-05.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

다음 코드의 출력으로 올바른 것은 무엇입니까?

```python
import torch

w = torch.tensor(2.0, requires_grad=True)
(w**2).backward()
(w**2).backward()
print(w.grad.item())
```

1. `0.0`
2. `4.0`
3. `8.0`
4. 실행 시 항상 `RuntimeError`가 발생합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

각 `w**2`의 미분값은 `2w = 4`입니다. PyTorch는 Gradient를 기본적으로 누적하므로 두 번의 `backward()` 실행 후 `w.grad`는 `4 + 4 = 8`이 됩니다. `w**2`를 매번 다시 계산해 서로 다른 그래프에서 역전파하므로 그래프 재사용 오류도 발생하지 않습니다.

**오답 해설**

- **①:** `backward()`는 기존 Gradient를 자동으로 초기화하지 않습니다.
- **②:** 한 번만 역전파한 값입니다.
- **④:** 코드의 두 연산은 서로 다른 계산 그래프를 만듭니다.

</details>

### Q-06.

**관련 개념:** [Chapter 05](../Chapter-05/README.md), [Chapter 06](../Chapter-06/README.md)

다음 중 추론 코드에 대한 설명으로 가장 적절한 것은 무엇입니까?

1. `model.eval()`은 모델의 파라미터에 저장된 Gradient를 모두 삭제합니다.
2. `torch.no_grad()`만 사용하면 Dropout이 자동으로 평가 모드로 바뀝니다.
3. `model.eval()`과 `torch.no_grad()`는 동일한 기능을 수행합니다.
4. `model.eval()`로 평가 동작을 설정하고, `torch.no_grad()`로 Gradient 기록을 비활성화할 수 있습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ④**

`model.eval()`은 Dropout이나 BatchNorm처럼 학습·평가 모드에 따라 동작이 달라지는 계층을 평가 모드로 전환합니다. `torch.no_grad()`는 실행 구간에서 Autograd의 그래프 기록을 비활성화합니다. 두 기능은 역할이 다르므로 일반적인 평가·추론에서는 함께 사용합니다.

**오답 해설**

- **①:** 모드를 바꾸는 것과 저장된 Gradient를 지우는 것은 다릅니다.
- **②:** `no_grad()`는 Dropout의 동작 모드를 바꾸지 않습니다.
- **③:** 역할이 다릅니다.

</details>

### Q-07.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

샘플 23개를 `DataLoader(batch_size=8, shuffle=False, drop_last=False)`로 처리했습니다. 각 배치의 샘플 수는 무엇입니까?

1. `8, 8, 8`
2. `8, 8, 7`
3. `8, 7, 7, 1`
4. `8, 8`이며 나머지 7개는 항상 버려집니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

23개를 8개씩 나누면 크기가 8인 배치 2개와 크기가 7인 배치 1개가 만들어집니다. `drop_last=False`이므로 마지막 배치도 처리합니다. Loss를 집계하거나 Gradient를 누적할 때는 이 배치의 실제 샘플 수도 고려해야 합니다.

</details>

### Q-08.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

PyTorch의 Custom Dataset에서 `__len__()`과 `__getitem__(index)`의 역할을 올바르게 설명한 것은 무엇입니까?

1. 두 함수 모두 반드시 GPU로 데이터를 이동시켜야 합니다.
2. `__len__()`은 전체 샘플 수를, `__getitem__()`은 지정된 인덱스의 샘플을 반환합니다.
3. `__len__()`은 배치 크기를, `__getitem__()`은 Epoch 수를 반환합니다.
4. 두 함수를 구현하면 `DataLoader`가 항상 데이터를 섞습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

일반적인 Map-style Dataset은 전체 샘플 수를 반환하는 `__len__()`과 지정된 인덱스의 샘플을 반환하는 `__getitem__()`을 구현합니다. 배치 구성과 데이터 섞기(Shuffle)는 주로 `DataLoader`에서 설정하며, GPU로 데이터를 옮기는 작업은 Dataset의 필수 역할이 아닙니다.

</details>

### Q-09.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

`torch.nn.Linear(4, 3, bias=True)`의 학습 가능한 파라미터 수는 얼마입니까?

1. 7개
2. 12개
3. 15개
4. 24개

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

Weight의 Shape는 `(out_features, in_features) = (3, 4)`이므로 원소가 12개입니다. Bias는 출력 뉴런마다 1개씩 있어 3개이며, 총 파라미터 수는 `12 + 3 = 15`개입니다.

</details>

### Q-10.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

다음 신경망에서 두 `Linear` 계층 사이에 ReLU 활성화 함수를 사용하는 주된 이유는 무엇입니까?

```python
import torch

model = torch.nn.Sequential(
    torch.nn.Linear(2, 8),
    torch.nn.ReLU(),
    torch.nn.Linear(8, 1),
)
```

1. 모든 파라미터를 고정하여 학습을 방지하기 위해서
2. 신경망이 선형 변환만으로 표현하기 어려운 비선형 관계를 학습할 수 있도록 하기 위해서
3. 입력 샘플 수를 자동으로 늘리기 위해서
4. `backward()` 호출 없이 Gradient를 계산하기 위해서

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

비선형 연산 없이 `Linear` 계층만 연결하면 전체를 하나의 아핀 변환(Affine Transformation)으로 표현할 수 있습니다. ReLU는 비선형성을 추가해 모델이 더 복잡한 관계를 학습하도록 돕습니다. 예를 들어 XOR 데이터는 하나의 직선으로 분리할 수 없습니다.

**오답 해설**

- **①:** ReLU는 파라미터를 고정하지 않습니다.
- **③:** ReLU는 샘플 수를 바꾸지 않습니다.
- **④:** 자동 미분이 활성화 함수를 대신하는 것은 아닙니다.

</details>

### Q-11.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

출력 계층이 `nn.Linear(8, 1)`이고 `forward()`에서 **Sigmoid를 적용하지 않은 Logit**을 반환합니다. 이진 분류 학습에 가장 적절한 방법은 무엇입니까?

1. `nn.BCEWithLogitsLoss()`에 Logit과 실수형 Target을 전달합니다.
2. Logit에 Softmax를 적용한 뒤 `nn.MSELoss()`만 사용해야 합니다.
3. `nn.CrossEntropyLoss()`를 사용하되 Target은 반드시 `(N, 1)` 실수형이어야 합니다.
4. Logit에 Sigmoid를 적용하고 다시 `nn.BCEWithLogitsLoss()`를 사용합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

`BCEWithLogitsLoss`는 Sigmoid와 이진 교차 엔트로피 계산을 수치적으로 안정적인 방식으로 결합합니다. Logit을 입력받으며, Target에는 Logit과 Shape가 같은 실수형 `0` 또는 `1`을 사용합니다.

**오답 해설**

- **②:** 이진 분류에 Softmax와 MSE 조합이 필요한 것은 아닙니다.
- **③:** 일반적인 두 클래스 Logit 출력의 `CrossEntropyLoss`는 `(N, 2)` Logit과 `(N,)` 정수형 클래스 인덱스를 사용합니다.
- **④:** Sigmoid를 미리 적용하면 Logit을 입력받아야 하는 Loss 함수에 확률을 전달하게 됩니다.

</details>

### Q-12.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

5개 클래스를 분류하는 모델의 배치 크기가 16일 때, `CrossEntropyLoss`를 올바르게 사용하는 방법은 무엇입니까?

1. 모델 출력 `(16, 5)` Logit, Target `(16,)` 정수형 클래스 인덱스
2. 모델 출력 `(16,)` Logit, Target `(16, 5)` 문자열 Label
3. 모델 출력 `(5, 16)` 확률, Target `(5,)` 실수형 Label
4. 모델 출력 `(16, 5)`에 Softmax를 반드시 적용한 뒤 `CrossEntropyLoss`를 호출

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

일반적인 단일 레이블 다중 분류에서는 샘플마다 클래스별 Logit 5개를 출력합니다. `CrossEntropyLoss`에는 `(N, C)` Shape의 Logit과 `(N,)` Shape의 `torch.long` 클래스 인덱스를 전달합니다. 내부적으로 LogSoftmax에 해당하는 계산을 수행하므로 Softmax를 미리 적용하지 않습니다.

</details>

### Q-13.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

Dropout을 포함한 MLP에서 동일한 입력에 대한 예측을 반복 실행했을 때 평가 모드에서 결과가 안정적으로 나오는 주된 이유는 무엇입니까?

1. `eval()`이 저장된 Weight를 모두 0으로 만들기 때문입니다.
2. 평가 모드에서는 Dropout의 무작위 제거가 적용되지 않기 때문입니다.
3. 평가 모드에서는 모든 텐서가 자동으로 CPU로 이동하기 때문입니다.
4. `eval()`을 호출하면 `optimizer.step()`이 자동으로 실행되기 때문입니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

Dropout은 학습 모드에서 일부 활성값을 무작위로 제거해 Overfitting을 줄이는 데 사용됩니다. 평가 모드에서는 Dropout이 비활성화되므로 입력과 Weight가 같고 연산이 결정적이라면 같은 결과가 나옵니다. 단, `eval()`만으로 Gradient 기록이 중단되지는 않습니다.

</details>

### Q-14.

**관련 개념:** [Chapter 07](../Chapter-07/README.md)

어떤 Epoch에서 샘플 4개인 배치의 평균 Loss가 `0.2`, 샘플 1개인 마지막 배치의 평균 Loss가 `0.8`이었습니다. 각 배치의 Loss가 샘플별 Loss의 평균일 때, 전체 Epoch 평균 Loss는 얼마입니까?

1. `0.20`
2. `0.30`
3. `0.32`
4. `0.50`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

배치 평균을 다시 단순 평균하면 `(0.2 + 0.8) / 2 = 0.5`입니다. 하지만 샘플마다 같은 비중을 주려면 배치 크기로 가중 평균해야 하므로 `(0.2 × 4 + 0.8 × 1) / 5 = 0.32`가 됩니다.

</details>

### Q-15.

**관련 개념:** [Chapter 07](../Chapter-07/README.md)

초기 학습률이 `0.1`이고 다음과 같이 Scheduler를 설정했습니다. `model`은 이미 정의되어 있다고 가정합니다. 매 Epoch 학습을 마친 뒤 `scheduler.step()`을 한 번 호출한다면, **두 번째 호출 직후**의 학습률은 얼마입니까?

```python
import torch

optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer, step_size=2, gamma=0.5
)
```

1. `0.1`
2. `0.05`
3. `0.025`
4. `0.5`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

`StepLR(step_size=2, gamma=0.5)`는 `scheduler.step()`을 두 번 호출할 때마다 학습률에 `0.5`를 곱합니다. 첫 번째 호출 직후에는 `0.1`, 두 번째 호출 직후에는 `0.05`가 됩니다. 일반적인 학습 루프에서는 해당 Epoch의 Optimizer 갱신을 마친 뒤 Scheduler를 실행합니다.

</details>

### Q-16.

**관련 개념:** [Chapter 07](../Chapter-07/README.md)

AdamW와 Scheduler를 사용하는 모델의 학습을 완료한 Epoch 다음부터 재개하려고 합니다. **가장 적절한 저장 방식**은 무엇입니까?

1. 모델의 `state_dict()`만 저장하면 Optimizer의 내부 상태와 Scheduler 진행 위치까지 항상 복원됩니다.
2. 최종 Test Accuracy만 기록하면 재학습 없이 같은 Weight를 얻을 수 있습니다.
3. 모델·Optimizer·Scheduler State와 완료한 Epoch, 필요한 난수·데이터 순서 상태를 함께 보관합니다.
4. 중단 후에는 모델을 반드시 처음부터 다시 초기화하고 Test 결과를 기준으로 최적 Epoch를 찾습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

학습을 이어서 수행하려면 모델 Weight뿐 아니라 Optimizer와 Scheduler의 내부 상태, 완료한 Epoch 정보를 저장해야 합니다. 데이터 순서와 Dropout에 사용된 난수 상태도 재현성에 영향을 줍니다. Epoch 경계에서 재개하는지, 배치 중간에서 재개하는지에 따라 필요한 저장 정보가 달라집니다.

**오답 해설**

- **①:** 모델 Weight만으로 Optimizer와 Scheduler의 상태가 복원되지는 않습니다.
- **②:** 평가 점수만으로는 모델 Weight나 학습 상태를 복원할 수 없습니다.
- **④:** Test 데이터를 반복적인 모델 선택에 사용하면 최종 평가의 독립성이 훼손됩니다.

</details>

## 주관식

### Q-17.

**관련 개념:** [Chapter 05](../Chapter-05/README.md), [Chapter 06](../Chapter-06/README.md)

다음 식에서 `y`와 `dy/dw`를 계산하고, PyTorch 코드로 Gradient를 확인하십시오.

```math
y = (wx+1)^2, \qquad w=2,\quad x=3
```


같은 Leaf Tensor에 `backward()`를 반복 실행할 때 주의할 점도 설명하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

```math
y = (2\cdot3+1)^2 = 49
```

Chain Rule을 적용하면 다음과 같습니다.

```math
\frac{dy}{dw} = 2(wx+1)x = 2\cdot7\cdot3 = 42
```

```python
import torch

w = torch.tensor(2.0, requires_grad=True)
x = torch.tensor(3.0)
y = (w * x + 1) ** 2
y.backward()
print(y.item())       # 49.0
print(w.grad.item())  # 42.0
```

PyTorch는 Leaf Tensor의 `.grad`에 Gradient를 누적합니다. 누적이 필요하지 않다면 다음 역전파 전에 `w.grad = None` 등으로 초기화해야 합니다. 같은 계산 그래프를 다시 역전파할 때는 그래프 재사용 가능 여부도 확인해야 합니다.

</details>

### Q-18.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

센서 측정값 `x`의 Shape는 `(2, 3)`입니다. 각 행에 채널별 보정값 `offsets = [1.0, -2.0, 0.5]`를 더한 뒤 유효한 값만 집계하려고 합니다. `NaN`은 유효하지 않은 값으로 처리합니다.

```python
import torch

x = torch.tensor([
    [10.0, 20.0, float("nan")],
    [12.0, 22.0, 30.0],
])
offsets = torch.tensor([1.0, -2.0, 0.5])
```

유효한 원소만 보정해 **채널별 유효 샘플 수와 평균**을 계산하는 코드를 작성하십시오. 유효값이 없는 채널의 처리 방침도 제시하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

```python
mask = torch.isfinite(x)
corrected = torch.where(mask, x, torch.zeros_like(x)) + offsets
corrected = torch.where(mask, corrected, torch.zeros_like(corrected))
counts = mask.sum(dim=0)
means = corrected.sum(dim=0) / counts.clamp_min(1)
means = torch.where(counts > 0, means, torch.full_like(means, float("nan")))
print(counts.tolist())  # [2, 2, 1]
print(means.tolist())   # [12.0, 19.0, 30.5]
```

`offsets`는 `x`의 마지막 차원 크기인 `3`과 일치하므로 Broadcasting됩니다. 유효하지 않은 값은 Mask로 합산에서 제외합니다. 유효값이 없는 채널은 예시처럼 `NaN`을 반환하거나 오류 상태로 처리할 수 있으며, 선택한 방침을 명확히 해야 합니다.

</details>

### Q-19.

**관련 개념:** [Chapter 05](../Chapter-05/README.md)

CSV 파일의 `temperature`, `pressure`, `failure` 세 열을 이용해 두 입력 특성과 하나의 이진 분류 Target을 반환하는 Custom Dataset을 설계하십시오. 다음 조건을 충족해야 합니다.

- 샘플 하나의 `x`는 `float32` 텐서이며 Shape는 `(2,)`입니다.
- Target `y`는 `float32` 텐서이며 Shape는 `(1,)`입니다.
- 배치 크기는 4이며 마지막 배치도 사용합니다.
- Dataset에 샘플이 10개 있을 때 배치별 Target Shape를 제시합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

```python
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

class SensorDataset(Dataset):
    def __init__(self, path):
        df = pd.read_csv(path)
        self.x = torch.tensor(
            df[["temperature", "pressure"]].to_numpy(dtype="float32")
        )
        self.y = torch.tensor(
            df[["failure"]].to_numpy(dtype="float32")
        )

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]

loader = DataLoader(SensorDataset("sensors.csv"), batch_size=4, shuffle=False)
```

배치별 Target Shape는 `(4, 1)`, `(4, 1)`, `(2, 1)`입니다. 실제 데이터를 사용할 때는 누락값과 자료형도 검증해야 합니다. Scaling을 적용한다면 평균과 표준편차는 Training 데이터에서만 계산해 데이터 누수를 방지해야 합니다.

</details>

### Q-20.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

입력 특성 3개, 은닉 뉴런 5개, 출력 Logit 2개인 MLP를 구성하십시오. 은닉층에는 ReLU를 사용하고, 모든 `nn.Linear` 계층에는 Bias를 포함합니다. 학습 가능한 파라미터의 총수와 입력 Shape가 `(7, 3)`일 때의 출력 Shape를 계산하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(3, 5), nn.ReLU(), nn.Linear(5, 2))
print(sum(p.numel() for p in model.parameters()))  # 32
print(model(torch.zeros(7, 3)).shape)               # torch.Size([7, 2])
```

첫 번째 `Linear` 계층은 `3×5+5=20`개, 두 번째 `Linear` 계층은 `5×2+2=12`개의 파라미터를 가집니다. ReLU에는 학습 가능한 파라미터가 없으므로 총 `32`개입니다.

</details>

### Q-21.

**관련 개념:** [Chapter 06](../Chapter-06/README.md)

샘플 6개로 구성된 배치가 있습니다. 이진 분류와 4개 클래스의 다중 분류에 적합한 **모델 출력 Shape, Target의 Shape·Dtype, Loss 함수**를 각각 제시하십시오. 해당 Loss 함수에 전달하기 전에 Sigmoid나 Softmax를 적용하면 안 되는 이유도 설명하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

| 구분 | 모델 출력 | Target | Loss |
|---|---|---|---|
| Binary | `(6, 1)` 실수형 Logit | `(6, 1)` `float32`의 0·1 | `nn.BCEWithLogitsLoss()` |
| Multiclass | `(6, 4)` 실수형 Logit | `(6,)` `torch.long`의 클래스 인덱스 0~3 | `nn.CrossEntropyLoss()` |

두 Loss 함수는 각각 Sigmoid 또는 LogSoftmax에 해당하는 계산을 내부에 포함합니다. 모델 출력에 미리 확률 변환을 적용하면 Loss 함수가 요구하는 Logit 대신 확률을 전달하게 되어 계산 결과와 수치 안정성에 영향을 줍니다. 추론 시 확률이 필요하다면 `torch.sigmoid()`나 `torch.softmax()`를 사용합니다.

</details>

### Q-22.

**관련 개념:** [Chapter 07](../Chapter-07/README.md)

샘플별 Loss의 평균을 반환하는 함수를 사용했습니다. 배치 크기가 `[4, 4, 2]`이고 각 배치의 평균 Loss가 `[0.2, 0.3, 0.8]`일 때, 전체 샘플 기준 Epoch 평균 Loss를 계산하고 코드로 구현하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

```math
L_{\mathrm{epoch}}=\frac{4\cdot0.2+4\cdot0.3+2\cdot0.8}{10}=0.36
```

```python
batch_sizes = [4, 4, 2]
batch_losses = [0.2, 0.3, 0.8]
weighted_total = sum(n * loss for n, loss in zip(batch_sizes, batch_losses))
epoch_loss = weighted_total / sum(batch_sizes)
print(f"{epoch_loss:.2f}")  # 0.36
```

배치 평균 Loss를 단순 평균하면 `(0.2 + 0.3 + 0.8) / 3 ≈ 0.4333`이 됩니다. 샘플별 Loss에 같은 비중을 주려면 배치 크기를 반영해 가중 평균해야 합니다.

</details>

### Q-23.

**관련 개념:** [Chapter 07](../Chapter-07/README.md)

샘플 5개를 크기가 `[2, 2, 1]`인 Micro-Batch로 나누었습니다. 샘플별 Loss의 평균을 구하는 `reduction="mean"`을 사용할 때, 전체 샘플을 하나의 배치로 처리한 것과 같은 평균 Gradient를 얻으려면 각 Micro-Batch의 Loss에 어떤 계수를 곱해야 합니까? 한 번의 Optimizer Update를 수행하는 코드 흐름도 설명하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

각 Micro-Batch의 평균 Loss에 `현재 Micro-Batch의 샘플 수 / 전체 샘플 수`를 곱합니다. 따라서 계수는 `2/5`, `2/5`, `1/5`입니다.

```python
optimizer.zero_grad(set_to_none=True)
for x_batch, y_batch in micro_batches:
    loss = criterion(model(x_batch), y_batch)
    (loss * (len(x_batch) / 5)).backward()
optimizer.step()
```

이 방식은 전체 샘플의 평균 Loss에서 계산한 Gradient와 일치하도록 보정한 것입니다. 다만 Dropout처럼 난수가 관여하거나 BatchNorm처럼 배치 통계에 의존하는 계층이 있으면 결과가 완전히 같지는 않을 수 있습니다. Gradient Clipping을 적용한다면 모든 Gradient를 누적한 뒤 `optimizer.step()` 직전에 한 번 적용해야 합니다.

</details>

### Q-24.

**관련 개념:** [Chapter 07](../Chapter-07/README.md)

AdamW, StepLR, Dropout을 사용하는 MLP를 20 Epoch 동안 학습하던 중 8번째 Epoch 종료 직후 프로그램이 중단되었습니다. 다음 Epoch부터 학습을 재개하려면 어떤 정보를 저장하고 복원해야 합니까? **Best Model 저장**과 **Resume Checkpoint 저장**의 목적도 비교하십시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범답안**

모델 Weight, AdamW의 Optimizer State, StepLR의 Scheduler State, 완료한 Epoch 번호, 난수 생성기의 상태를 저장해야 합니다. 데이터 순서에 영향을 주는 Generator나 Sampler의 상태도 재현성에 필요할 수 있습니다. Early Stopping을 사용했다면 최적 검증 점수와 Epoch, Patience Counter도 함께 보관합니다.

Epoch가 끝난 시점부터 재개할 때는 다음 Epoch의 데이터 순서가 기존 실행과 같아야 합니다. 배치 중간에서 재개한다면 해당 Epoch의 샘플 순서, 처리한 배치 위치, 필요한 경우 누적 Gradient까지 복원해야 합니다.

**Best Model**은 검증 성능이 가장 좋았던 Weight를 최종 평가나 추론에 사용하기 위해 저장합니다. **Resume Checkpoint**는 학습을 중단된 지점부터 이어가기 위한 파일로, Optimizer와 Scheduler 등의 진행 상태를 포함합니다. 두 파일의 목적은 서로 다릅니다.

</details>

---

[← Summary 목차](./README.md) · [Problems](./problem.md) · [AI 목차](../README.md)
