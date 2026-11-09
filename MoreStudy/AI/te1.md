# Problems — Summary Part 02

Chapter 05~07 · **Basic 5 · Advanced 4 · Professional 3 · Challenge 2 · Radiant 1**

각 문제의 입력·출력 조건을 충족하는 Python 프로그램을 작성하시오. 예제는 공개된 검증 사례이며, 예제만 통과하는 코드는 완성된 구현으로 간주하지 않습니다. 관련 개념과 구현 가이드는 필요할 때 확인할 수 있습니다.

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)

## Basic

### B-01. Tensor Inspector — Tensor 구조와 집계

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Tensor · Shape · Dtype · Reduction

#### 문제 설명

센서 장비에서 수집한 수치 데이터가 행렬 형태로 전달됩니다. 데이터가 올바른 Shape를 갖는지 확인하고, 채널별 합계와 Sample별 평균을 계산해야 합니다.

주어진 수치 데이터를 `torch.float32` Tensor로 생성한 뒤 Tensor 연산으로 요약 정보를 계산하는 프로그램을 작성하시오.

#### 요구사항

1. 입력에서 Sample 수 `N`과 채널 수 `D`를 읽고 Shape `(N, D)`의 Tensor를 생성합니다.
2. 채널별 합계는 `dim=0`, Sample별 평균은 `dim=1`을 사용하여 계산합니다.
3. 결과를 지정된 출력 형식으로 표시합니다. 수치 출력은 소수점 둘째 자리까지 표시합니다.
4. 입력 행 수, 열 수, 숫자 형식 또는 값의 유한성에 문제가 있으면 `INVALID`만 출력합니다.

#### 입력

첫 줄에 `N D`가, 다음 `N`개 줄에 각각 `D`개의 실수가 공백으로 구분되어 주어집니다.

- `1 ≤ N ≤ 200`, `1 ≤ D ≤ 20`
- 정수처럼 표기된 값도 실수로 읽습니다.
- `NaN`, 무한대 및 추가 데이터 행은 허용하지 않습니다.

#### 출력

```text
SHAPE N D
DTYPE float32
COLUMN_SUM 값1 값2 ...
ROW_MEAN 값1 값2 ...
```

**예제 입력**

```text
2 3
1 2 3
4 5 6
```

**예제 출력**

```text
SHAPE 2 3
DTYPE float32
COLUMN_SUM 5.00 7.00 9.00
ROW_MEAN 2.00 5.00
```

#### 검증 항목 (Edge Cases)

- `N=1`, `D=1`에서 차원이 사라지지 않는지 확인
- 빈 행, 누락된 원소, 초과된 원소, 잘못된 숫자를 정확히 거부하는지 확인
- 합계와 평균이 올바른 차원에 대해 계산되는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **입력 검증:** 행마다 정확히 `D`개의 값이 있는지 확인하고 `math.isfinite()`로 유한성을 검사합니다.
2. **Tensor 변환:** `torch.tensor(rows, dtype=torch.float32)`로 생성한 뒤 `.shape`를 확인합니다.
3. **차원별 집계:** `tensor.sum(dim=0)`과 `tensor.mean(dim=1)`을 사용합니다. 출력 형식은 `f"{value:.2f}"`로 통일합니다.

</details>

---

### B-02. Channel Calibration — Broadcasting을 이용한 측정값 보정

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Broadcasting · Element-wise Operations · Reduction

#### 문제 설명

하나의 장비가 여러 센서 채널을 동시에 측정합니다. 센서마다 영점 보정값과 배율이 다르므로, 반복문으로 개별 채널을 처리하기보다 Tensor의 Broadcasting을 활용하려고 합니다.

각 입력값에 아래 식을 적용하여 보정된 행렬과 채널별 평균을 출력하시오.

\[
z_{ij}=(x_{ij}+o_j)s_j
\]

- `x_ij`: `i`번째 Sample의 `j`번째 채널 측정값
- `o_j`: 채널 `j`의 Offset
- `s_j`: 채널 `j`의 Scale

#### 요구사항

1. 측정값 행렬의 Shape는 `(N, D)`, Offset과 Scale의 Shape는 `(D,)`로 구성합니다.
2. Broadcasting으로 전체 행렬을 한 번에 보정합니다.
3. 보정된 Sample을 원래 순서대로 출력하고, 채널별 보정 평균을 계산합니다.
4. Offset·Scale의 길이가 맞지 않거나 Scale이 0 이하이면 `INVALID`를 출력합니다.

#### 입력

첫 줄에 `N D`, 두 번째 줄에 `D`개의 Offset, 세 번째 줄에 `D`개의 Scale이 주어집니다. 이어서 `N`개 측정값 행이 주어집니다.

- `1 ≤ N ≤ 200`, `1 ≤ D ≤ 20`
- 모든 값은 유한한 실수, 모든 Scale은 양수입니다.

#### 출력

보정된 행은 `SAMPLE_i`로, 채널별 평균은 `CHANNEL_MEAN`으로 시작합니다. 모든 수치는 소수점 둘째 자리까지 표시합니다.

**예제 입력**

```text
2 2
1 -2
2 0.5
10 20
12 30
```

**예제 출력**

```text
SAMPLE_1 22.00 9.00
SAMPLE_2 26.00 14.00
CHANNEL_MEAN 24.00 11.50
```

#### 검증 항목 (Edge Cases)

- Offset과 Scale을 Sample 축이 아닌 채널 축에 적용했는지 확인
- 단일 Sample 또는 단일 채널에서도 Broadcasting이 올바르게 동작하는지 확인
- Shape 불일치, 음수 Scale, 무한대 입력 처리

<details>
<summary><strong>구현 가이드</strong></summary>

1. `x`, `offsets`, `scales`를 `torch.float32`로 구성합니다.
2. 다음과 같이 연산합니다.

```python
corrected = (x + offsets) * scales
channel_mean = corrected.mean(dim=0)
```

3. 별도의 중첩 반복문으로 연산 결과를 만들기보다 Tensor 연산 결과를 출력에만 순회합니다.

</details>

---

### B-03. First Autograd Step — 첫 번째 Gradient 계산과 갱신

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Autograd · Gradient · [Chapter 06](../Chapter-06/README.md) · Loss

#### 문제 설명

하나의 입력 `x`와 정답 `y`에 대해 선형 모델 `wx+b`의 예측 오차를 구하고, Gradient를 계산하여 Parameter를 한 번 갱신합니다. 여러 Epoch을 학습하는 문제가 아니라, Autograd가 어떤 값을 계산하고 갱신에 어떻게 사용되는지 확인하는 문제입니다.

\[
\hat y=wx+b,\quad L=(\hat y-y)^2
\]

\[
w_{\mathrm{new}}=w-\eta\frac{\partial L}{\partial w},\quad
b_{\mathrm{new}}=b-\eta\frac{\partial L}{\partial b}
\]

#### 요구사항

1. `w`, `b`를 `requires_grad=True`인 Scalar Tensor로 생성합니다.
2. 예측값과 Loss를 계산한 뒤 `backward()`를 한 번 호출합니다.
3. `w.grad`와 `b.grad`를 출력합니다.
4. `torch.no_grad()` 문맥에서 Parameter를 한 번 갱신한 뒤 새 예측값을 출력합니다.
5. 계산 순서가 달라지지 않도록 Gradient와 원래 Loss는 갱신 전에 기록합니다.

#### 입력

한 줄에 `w b x y eta`가 주어집니다. `eta`는 `0 < eta ≤ 1`이고 모든 값은 유한한 실수입니다. 계산은 `float64`로 수행합니다.

#### 출력

수치는 소수점 넷째 자리까지 표시합니다. 유효하지 않은 입력은 `INVALID`를 출력합니다.

**예제 입력**

```text
1 0 2 5 0.1
```

**예제 출력**

```text
PREDICTION 2.0000
LOSS 9.0000
GRAD_W -12.0000
GRAD_B -6.0000
UPDATED_W 2.2000
UPDATED_B 0.6000
UPDATED_PREDICTION 5.0000
```

#### 검증 항목 (Edge Cases)

- `x=0`일 때 Weight Gradient가 0이 되는지 확인
- 예측이 정확하여 Loss가 0인 경우 Gradient도 0인지 확인
- `backward()`를 중복 호출해 Gradient를 누적하지 않는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. `torch.tensor(float_value, dtype=torch.float64, requires_grad=True)`로 Parameter를 생성합니다.
2. `loss.backward()` 후 `.grad.item()`으로 Gradient를 읽습니다.
3. Parameter 갱신은 계산 그래프를 기록하지 않도록 처리합니다.

```python
with torch.no_grad():
    w -= eta * w.grad
    b -= eta * b.grad
```

손계산으로는 `dL/dw = 2(wx+b-y)x`, `dL/db = 2(wx+b-y)`를 이용해 결과를 확인할 수 있습니다.

</details>

---

### B-04. MLP Architecture Inspector — 신경망 구조와 Parameter 수

**관련 개념:** [Chapter 06](../Chapter-06/README.md) · `nn.Linear` · ReLU · Parameter Count · Forward

#### 문제 설명

입력 Feature 수, 은닉 뉴런 수, 출력 수가 주어졌을 때 `Linear → ReLU → Linear` 구조의 MLP를 구성합니다. 모델을 학습하지 않고, 구성한 신경망의 출력 Shape와 학습 가능한 Parameter 수가 예상대로인지 확인하시오.

#### 요구사항

1. `nn.Sequential(nn.Linear(D, H), nn.ReLU(), nn.Linear(H, O))`를 구성합니다. 두 Linear Layer 모두 Bias를 사용합니다.
2. 첫 Layer와 두 번째 Layer의 Parameter 수를 구합니다.
3. Batch Size `N`의 영(0) Tensor를 입력하여 Forward 결과의 Shape를 확인합니다.
4. 입력 범위가 잘못되면 `INVALID`를 출력합니다.

#### 입력

한 줄에 `N D H O`가 주어집니다. 모든 값은 정수이며 각각 `1 ≤ N ≤ 256`, `1 ≤ D,H,O ≤ 128`입니다.

#### 출력

```text
LAYER_1_PARAMETERS 값
LAYER_2_PARAMETERS 값
TOTAL_PARAMETERS 값
OUTPUT_SHAPE N O
```

**예제 입력**

```text
5 3 4 2
```

**예제 출력**

```text
LAYER_1_PARAMETERS 16
LAYER_2_PARAMETERS 10
TOTAL_PARAMETERS 26
OUTPUT_SHAPE 5 2
```

#### 검증 항목 (Edge Cases)

- Bias를 빠뜨리지 않고 계산하는지 확인
- `nn.Linear`의 Weight Shape가 `(out_features, in_features)`임을 반영했는지 확인
- 출력 Shape를 실제 Forward 실행으로 검사하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

첫 Layer는 `D×H+H`, 두 번째 Layer는 `H×O+O`개입니다. 모델에서 Parameter를 직접 계산할 때는 다음 코드를 활용할 수 있습니다.

```python
counts = [sum(p.numel() for p in layer.parameters()) for layer in (model[0], model[2])]
```

ReLU는 학습 가능한 Parameter가 없습니다. 임의 초기 Weight의 출력 수치를 정답으로 고정하지 않고 출력 Shape만 검증합니다.

</details>

---

### B-05. DataLoader Batch Trace — Mini-Batch 구성

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · TensorDataset · DataLoader · Batch Size · `drop_last`

#### 문제 설명

학생은 데이터가 DataLoader를 통과할 때 실제로 어떤 순서와 크기의 Batch로 묶이는지 확인하려고 합니다. 정해진 Sample ID를 순서대로 불러오고, 마지막 Batch 처리 규칙을 출력하시오.

#### 요구사항

1. 입력된 ID를 `torch.long` Tensor로 만든 뒤 `TensorDataset`과 `DataLoader`를 사용합니다.
2. `shuffle=False`, 지정된 `batch_size=B`, 지정된 `drop_last` 옵션을 적용합니다.
3. 생성된 Batch 개수, 각 Batch의 ID 목록, 사용하지 않은 Sample 수를 출력합니다.
4. 입력에 오류가 있으면 `INVALID`를 출력합니다.

#### 입력

첫 줄에 `N B drop_last`가, 다음 줄에 서로 다른 정수형 ID `N`개가 주어집니다.

- `1 ≤ N ≤ 200`, `1 ≤ B ≤ 200`
- `drop_last`는 `0` 또는 `1`입니다.

#### 출력

`drop_last=1`일 경우 불완전한 마지막 Batch는 생성하지 않습니다.

**예제 입력**

```text
7 3 0
10 20 30 40 50 60 70
```

**예제 출력**

```text
BATCHES 3
BATCH_1 10 20 30
BATCH_2 40 50 60
BATCH_3 70
DROPPED 0
```

#### 검증 항목 (Edge Cases)

- `N`이 `B`로 나누어떨어지지 않는 경우
- `B > N`이면서 `drop_last=1`인 경우 (`BATCHES 0`)
- 중복 ID, 잘못된 Flag, 부족하거나 초과된 입력값

<details>
<summary><strong>구현 가이드</strong></summary>

```python
from torch.utils.data import DataLoader, TensorDataset

loader = DataLoader(
    TensorDataset(torch.tensor(ids, dtype=torch.long)),
    batch_size=batch_size,
    shuffle=False,
    drop_last=bool(drop_last),
)
```

DataLoader가 반환하는 Batch에서 첫 번째 원소인 ID Tensor를 사용합니다. Batch 수는 `len(loader)`로 확인할 수 있으며 사용하지 않은 Sample 수는 전체 ID 수에서 실제 사용한 수를 빼면 됩니다.

</details>

---

## Advanced

### A-01. Sensor Tensor Quality Pipeline — 센서 보정과 데이터 품질 보고

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Tensor · Broadcasting · Mask · Data Validation

#### 문제 설명

시설 운영 시스템은 각 공간의 온도·습도·전력 사용량을 수집합니다. 센서마다 보정값이 다르고 일부 기록에는 누락값과 범위 오류가 있습니다. 잘못된 기록이 통계에 포함되면 보고서의 평균값도 달라지므로, 먼저 데이터를 검증한 뒤 보정과 집계를 수행해야 합니다.

주어진 두 CSV를 읽어 정상 기록만 Tensor로 구성하고, 채널별 보정과 집계 결과를 생성하는 프로그램을 작성하시오.

#### 요구사항

1. `sensor_readings.csv`의 필수 열과 값의 유효성을 검사합니다. `record_id`는 공백이 없는 고유 문자열이어야 하며, `room_id`는 비어 있으면 안 됩니다.
2. 측정값의 허용 범위는 `-40 ≤ temperature ≤ 100`, `0 ≤ humidity ≤ 100`, `power_kw ≥ 0`입니다. 값은 모두 유한한 실수여야 합니다.
3. 오류 우선순위는 **필수값 누락 → 잘못된 숫자 또는 범위 → 유효한 ID 중복** 순서로 정합니다. 무효 행은 ID를 점유하지 않습니다.
4. `calibration.csv`에서 세 Feature의 Offset과 Scale을 읽습니다. Feature는 `temperature`, `humidity`, `power_kw`가 정확히 한 번씩 있어야 하며 Scale은 양수입니다. 보정식은 `z=(x+offset)*scale`입니다.
5. 정상 측정값을 Shape `(N, 3)`의 `float32` Tensor로 변환하고 Broadcasting으로 보정합니다.
6. `calibrated.csv`, `rejected_rows.csv`, `quality_report.json`을 생성합니다. 정상 Sample이 5개 미만이면 보고용 모델 입력을 만들지 않고 명시적으로 중단합니다.

#### 입력 파일 규격

**`sensor_readings.csv`**

```csv
record_id,room_id,temperature,humidity,power_kw
R01,LAB-A,20,50,3
R02,LAB-A,22,55,4
R03,LAB-B,,80,2
```

**`calibration.csv`**

```csv
feature,offset,scale
temperature,1,1
humidity,-5,1
power_kw,0,2
```

위 두 파일은 데이터 형식 예시이며, 실제 프로젝트 데이터에는 정상 기록이 5개 이상 포함됩니다.

#### 출력 파일 규격

- `calibrated.csv`: `record_id,room_id,temperature,humidity,power_kw` 순서. 정상 행은 원본 순서 유지, 실수는 소수점 넷째 자리까지 기록
- `rejected_rows.csv`: `source_line,record_id,error_code` 순서. 헤더를 1행으로 세어 입력 행 번호를 기록. 코드는 `MISSING_VALUE`, `INVALID_NUMBER`, `DUPLICATE_ID`
- `quality_report.json`: `valid_count`, `rejected_count`, `shape`, `channel_mean`의 네 항목. `shape`는 `[N,3]`, `channel_mean`에는 위 세 Feature의 보정 평균을 기록

**예제 처리 결과**

`R01`의 보정값은 `[21,45,6]`, `R02`는 `[23,50,8]`입니다. `R03`은 온도 누락으로 거부됩니다. 제시된 세 행은 전체 프로젝트의 정상 Sample 최소 수를 충족하지 못하므로 완성 프로그램에서는 최소 수 조건을 보고해야 합니다.

#### 검증 항목 (Edge Cases)

- 정상 행 이전에 등장한 무효 ID가 이후 정상 행을 잘못 차단하지 않는지 확인
- `NaN`, `Infinity`, 누락 열, 중복 Calibration Feature를 거부하는지 확인
- Feature 순서를 고정하고 Tensor의 행·열 차원을 올바르게 유지하는지 확인
- 통계는 유효한 보정 데이터만 이용해 계산하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. Schema 및 행 검증:** `dtype=str`로 읽어 원본 값을 보존하고, 숫자 변환과 범위 검사를 명시적으로 수행합니다. 무효 행은 `source_line`과 오류 코드로 기록합니다.

**STEP 2. Tensor 변환과 보정:** 정상 행에서 고정된 Feature 순서의 배열을 만듭니다.

```python
features = ["temperature", "humidity", "power_kw"]
values = torch.tensor(valid_df[features].to_numpy(dtype="float32"))
offsets = torch.tensor(offset_values, dtype=torch.float32)
scales = torch.tensor(scale_values, dtype=torch.float32)
calibrated = (values + offsets) * scales
```

**STEP 3. 결과 검사:**Tensor Shape, 평균, CSV 행 수, 거부 행 수를 각각 확인합니다. 보고서 평균은 원본 값이 아닌 보정값을 기준으로 계산합니다.

</details>

---

### A-02. Binary MLP Training — 신경망 분류와 독립 평가

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Dataset · DataLoader · [Chapter 06](../Chapter-06/README.md) · MLP · `BCEWithLogitsLoss` · [Chapter 07](../Chapter-07/README.md) · Training Loop

#### 문제 설명

시설의 두 가지 이용 지표로 혼잡 여부를 판단하려고 합니다. 데이터는 단순한 직선 하나로 구분하기 어려운 패턴을 포함합니다. 분류 모델을 학습하기 전에 Train·Validation·Test를 분리하고, 간단한 Baseline과 비교할 필요가 있습니다.

PyTorch로 작은 MLP를 학습하고, 고정된 Test Data에서 예측 결과를 기록하는 프로그램을 작성하시오.

#### 요구사항

1. `usage.csv`의 `split` 값(`train`, `validation`, `test`)을 그대로 사용합니다. 행을 다시 임의로 분할하지 않습니다.
2. Model 입력 Feature는 `x1`, `x2` 두 개이며, Target `crowded`는 `0` 또는 `1`입니다. 각 분할에는 두 클래스가 모두 존재한다고 가정합니다.
3. Training Data만 사용해 Feature별 평균과 표준편차를 계산하고, 세 분할에 같은 기준을 적용합니다. 표준편차가 0인 Feature는 Scale을 1로 처리합니다.
4. `nn.Linear(2,12) → nn.ReLU() → nn.Linear(12,1)` 구조를 구현합니다.
5. `BCEWithLogitsLoss`, `AdamW(lr=0.01)`, Batch Size 16, 최대 100 Epoch, `torch.manual_seed(42)`를 사용합니다. Epoch마다 DataLoader를 사용하고 마지막 Batch를 버리지 않습니다.
6. 매 Epoch의 Training 평균 Loss와 Validation Accuracy를 기록합니다. **최종 선택 기준은 Validation Accuracy 최대, 동점이면 더 이른 Epoch** 로 정합니다.
7. Training Data에서 가장 빈번한 클래스를 항상 예측하는 Majority Baseline도 계산합니다. 빈도가 같다면 `0`을 선택합니다.
8. Test 결과에 대한 Accuracy·F1·Confusion Matrix를 계산하고, `test_predictions.csv`를 생성합니다. 예측 Label은 `torch.sigmoid(logit) ≥ 0.5`로 결정합니다. Test 결과를 보고 모델을 다시 선택하지 않습니다.

#### 입력 파일 규격

**`usage.csv`**

```csv
record_id,split,x1,x2,crowded
U001,train,-1.2,0.8,1
U002,train,0.4,0.5,0
U003,validation,1.1,-0.9,1
U004,test,-0.2,-0.3,0
```

실제 실습 데이터에는 Train·Validation·Test가 각각 30개 이상 포함되고 `record_id`는 전체에서 유일합니다. Feature는 유한한 실수입니다.

#### 출력 파일 규격

- `training_history.csv`: `epoch,train_loss,validation_accuracy`
- `model_selection.json`: `best_epoch,best_validation_accuracy,train_majority_class,test_baseline_accuracy`
- `test_predictions.csv`: `record_id,actual,probability,predicted` (Test 원본 순서 유지, 확률 소수점 넷째 자리)
- `test_metrics.json`: `accuracy,f1,tp,fp,fn,tn` (계산은 반올림 전 확률 기준)

고정된 예측 확률이나 Accuracy는 정답값으로 제시하지 않습니다. Seed와 환경, 학습 절차가 같아도 라이브러리·하드웨어에 따른 미세한 차이가 가능하기 때문입니다.

#### 검증 항목 (Edge Cases)

- Train만으로 계산한 Scaling 기준을 Validation·Test에 적용하는지 확인
- Loss에 Sigmoid가 중복 적용되지 않는지 확인
- 마지막 Batch의 크기에 맞춰 Training Loss를 집계하는지 확인
- Model Selection은 Validation으로 수행하고 Test는 한 번만 평가하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. Dataset 구성:** 분리된 DataFrame을 `float32` Tensor로 변환하고 `TensorDataset`을 사용합니다. Target Shape는 `(N,1)`로 유지합니다.

**STEP 2. Training Loop:**

```python
for x_batch, y_batch in train_loader:
    optimizer.zero_grad(set_to_none=True)
    logits = model(x_batch)
    loss = criterion(logits, y_batch)
    loss.backward()
    optimizer.step()
```

**STEP 3. Validation:** `model.eval()`과 `torch.no_grad()`를 사용합니다. 가장 높은 Validation Accuracy의 `state_dict`를 **복사하여 보관** 합니다. 단순히 변수에 모델 객체를 참조해 두면 이후 학습에 따라 값이 바뀔 수 있습니다.

**STEP 4. Test:**Best Weight를 복원한 뒤 확률과 예측 Label을 계산합니다. Accuracy·F1은 별도 기준으로 검증합니다.

</details>

---

### A-03. Controlled Optimizer Comparison — Optimizer 비교 실험

**관련 개념:** [Chapter 07](../Chapter-07/README.md) · SGD · AdamW · Learning Rate · Fair Comparison · Reproducibility

#### 문제 설명

데이터센터의 전력 사용량을 예측하는 MLP를 학습하려고 합니다. 학습이 빠르게 진행되는 설정을 찾는 것도 중요하지만, 서로 다른 Optimizer를 비교하면서 초기 Weight나 데이터 순서가 달라지면 결과를 해석하기 어렵습니다.

두 학습 설정을 **동일한 초기 Parameter, 데이터 분할, Epoch 수, Batch 순서** 에서 비교하는 실험 프로그램을 작성하시오.

#### 요구사항

1. `energy.csv`에 명시된 `train`, `validation`, `test` 분할을 유지합니다. Training Data에서만 Feature Scaling 기준을 학습합니다.
2. 입력 Feature는 `occupancy`, `temperature_c`, `weekend`이고 Target은 `energy_kwh`입니다. 회귀 MLP는 `Linear(3,16) → ReLU → Linear(16,1)`입니다.
3. 같은 Seed 42로 생성한 초기 `state_dict`를 두 후보에 각각 복사합니다. Epoch별 Shuffle 순서도 두 후보에 동일하게 적용합니다.
4. 후보 A는 `SGD(lr=0.02, momentum=0.9)`, 후보 B는 `AdamW(lr=0.01, weight_decay=0.01)`입니다. 이 비교는 **Optimizer와 학습률을 포함한 두 설정의 비교** 이지, Optimizer 종류만 바꾸는 통제 실험은 아닙니다.
5. Batch Size 16, 최대 30 Epoch, MSELoss로 학습합니다. Epoch 평균 Loss는 Sample 수를 반영합니다.
6. 매 Epoch의 Validation RMSE를 기록하고 후보별 최고 Weight를 별도로 보관합니다.
7. 가장 작은 후보별 최고 Validation RMSE를 얻은 설정을 선택합니다. 동점은 후보 A를 선택합니다. Test는 선정된 설정의 Best Weight로 한 번만 평가합니다.

#### 입력 파일 규격

**`energy.csv`**

```csv
record_id,split,occupancy,temperature_c,weekend,energy_kwh
E001,train,35,20,0,96
E002,train,61,23,0,129
E003,validation,47,22,1,114
E004,test,53,19,0,120
```

- `record_id`는 고유, `weekend`는 0 또는 1, `occupancy`와 `energy_kwh`는 0 이상의 유한한 실수입니다.
- 각 분할은 최소 30개 Sample을 포함합니다.

#### 출력 파일 규격

- `training_history.csv`: `candidate,epoch,train_loss,validation_rmse`
- `comparison.json`: 각 후보의 `optimizer`, `learning_rate`, `best_epoch`, `best_validation_rmse`, 선정된 후보 `selected_candidate`
- `test_predictions.csv`: `record_id,actual,predicted`
- `test_metrics.json`: 선정된 모델의 `mae,rmse`

Test 점수는 후보 선택 기준에 사용할 수 없습니다. 모델 비교 결과에 대한 해석에는 학습률이 서로 다르다는 사실을 반드시 포함합니다.

#### 검증 항목 (Edge Cases)

- 첫 Epoch 전에 두 후보의 Parameter가 실제로 동일한지 확인
- 동일한 Sample 순서를 사용했는지, Optimizer 상태가 후보 간 공유되지 않는지 확인
- Training·Validation Loss와 RMSE를 혼동하지 않고 집계했는지 확인
- Best Epoch가 마지막 Epoch가 아닐 때도 해당 Weight로 Test를 수행하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 공통 초기 상태 복사:**

```python
import copy

torch.manual_seed(42)
initial_model = make_model()
initial_state = copy.deepcopy(initial_model.state_dict())
```

**STEP 2. 후보별 학습:** 각 후보를 새 모델·새 Optimizer로 만들고 `load_state_dict(initial_state)`를 적용합니다. Epoch별 `torch.Generator().manual_seed(42 + epoch)` 등의 방식으로 동일한 Sample 순서를 확보합니다.

**STEP 3. 공정한 비교:** 동일한 데이터, Epoch 예산, 모델 구조를 사용하되 서로 다른 Learning Rate를 포함한 설정을 비교한다는 점을 명시합니다. Validation으로 Best Weight를 결정하고 Test에 대한 재조정은 하지 않습니다.

</details>

---

### A-04. Reliable Model Handoff — 학습 모델 저장과 추론 정합성 검증

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Dtype · Device · [Chapter 06](../Chapter-06/README.md) · `state_dict` · Inference · [Chapter 07](../Chapter-07/README.md) · Reproducibility

#### 문제 설명

실험 환경에서 모델을 학습한 뒤 다른 담당자가 예측을 실행하려고 합니다. 단순히 Weight 파일만 전달하면 학습 때 사용한 Feature 순서나 Scaling 기준이 달라져 결과가 바뀔 수 있습니다.

학습과 추론을 **서로 다른 실행 과정으로 분리** 하고, 저장·복원 후에도 같은 입력에 대해 일관된 예측을 얻도록 프로그램을 작성하시오.

#### 요구사항

1. `training.csv`의 `split`을 유지합니다. Feature는 `temperature_c`, `vibration`, `hours_active` 세 개이고 Binary Target은 `needs_service`입니다.
2. Training Data에서만 평균·표준편차를 구하고 표준편차가 0인 열은 1로 처리합니다.
3. `Linear(3,8) → ReLU → Linear(8,1)` 모델을 만들고 `BCEWithLogitsLoss`, `AdamW(lr=0.01)`로 최대 50 Epoch 학습합니다. Best Validation Loss를 기준으로 Weight를 선택합니다.
4. 모델의 `state_dict`를 `model_weights.pt`에 저장하고 Feature 순서·Scaling 기준·Target·예측 Threshold 0.5를 `preprocessing.json`에 기록합니다.
5. 별도 `predict` 실행에서는 학습 CSV를 읽지 않고 저장 파일과 `incoming.csv`만 사용합니다. CSV 열의 순서가 달라져도 **이름을 기준으로** 동일한 Feature 순서를 복원합니다.
6. 신규 데이터의 필수 Feature 누락, 유효하지 않은 숫자, 중복 `record_id`는 행별로 거부하고 사유를 남깁니다. 필수 열 자체가 누락되었으면 추론을 중단합니다.
7. 원래 모델과 새 프로세스에서 복원한 모델의 동일 Test 입력에 대한 확률 차이는 CPU 환경에서 `1e-6` 이하여야 합니다.

#### 입력 파일 규격

**`training.csv`**

```csv
record_id,split,temperature_c,vibration,hours_active,needs_service
T01,train,30,2.1,180,0
T02,train,42,5.8,260,1
T03,validation,37,4.0,230,1
T04,test,32,2.5,210,0
```

**`incoming.csv`** (Feature 순서를 바꾼 예시)

```csv
record_id,hours_active,temperature_c,vibration
N01,220,34,3.1
N02,280,44,6.2
```

#### 출력 파일 규격

- `model_weights.pt`, `preprocessing.json`
- `test_predictions.csv`: `record_id,actual,probability,predicted`
- `incoming_predictions.csv`: `record_id,probability,predicted`
- `rejected_rows.csv`: `record_id,error_code` (`INVALID_VALUE`, `DUPLICATE_ID`)
- `handoff_report.json`: `feature_order`, `test_accuracy`, `reload_max_abs_diff`

확률은 파일에 소수점 여섯째 자리까지 기록하되, 복원 일치 여부는 **반올림 전** 값을 비교합니다. `torch.load()`는 프로젝트가 직접 생성한 신뢰 가능한 파일에 한해 `weights_only=True`를 사용합니다.

#### 검증 항목 (Edge Cases)

- `incoming.csv`의 열 순서가 달라도 예측이 일치하는지 확인
- `eval()`과 `no_grad()`를 적용했는지 확인
- 잘못된 `Dtype`·`Shape`, 누락 Feature, 복원되지 않은 Scaling 기준을 정확하게 감지하는지 확인
- 저장한 Best Weight가 마지막 Epoch의 Weight와 다를 수 있음을 반영했는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 학습 산출물 보관:**

```python
feature_order = ["temperature_c", "vibration", "hours_active"]
torch.save(best_state, "model_weights.pt")
```

Scaling 기준은 JSON에서 Feature 이름과 순서를 함께 보관합니다. Dataset을 다시 읽을 필요가 없도록 모델 구조와 Dtype도 명시합니다.

**STEP 2. 분리된 추론 과정:**

```python
model = make_model()
state = torch.load("model_weights.pt", map_location="cpu", weights_only=True)
model.load_state_dict(state)
model.eval()
with torch.inference_mode():
    logits = model(x)
    probabilities = torch.sigmoid(logits)
```

**STEP 3. 정합성 검증:** 원래 모델과 복원한 모델에 동일한 **정렬된 Feature 배열** 을 입력하여 반올림 전 확률을 비교합니다.

</details>

---
## Professional

### P-01. Fleet Maintenance Risk Training — 정비 위험 예측 모델의 학습 및 운영 정책 설계

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · DataLoader · [Chapter 06](../Chapter-06/README.md) · Binary MLP · [Chapter 07](../Chapter-07/README.md) · `pos_weight` · Early Stopping · Group Split · Threshold

#### 문제 설명

여러 사업장의 설비에서 온도, 진동과 경보 횟수가 수집됩니다. 정비팀은 향후 7일 안에 고장이 발생할 위험이 높은 설비를 미리 확인하려고 합니다. 실제 고장은 드물고, 같은 사업장의 장비는 사용 환경을 공유합니다. 단순한 무작위 분할은 새로운 사업장에서의 성능을 과대평가할 수 있습니다.

이번 과제에서는 **PyTorch 학습 파이프라인** 을 구축하고, 불균형 데이터의 Loss 설계와 Early Stopping, 사업장 단위 평가, 제한된 정비 인력에 맞춘 경보 정책을 연결합니다.

#### 제공 데이터

모든 CSV는 UTF-8이고 실습용 합성 데이터입니다. 과거 기록은 최소 12개 사업장과 400개 이상의 유효 Sample을 포함합니다.

**`maintenance_history.csv`**

| 열 이름 | 의미 | 사용 기준 |
|---|---|---|
| `record_id` | 관측 기록 ID | 중복 확인·결과 추적 |
| `site_id` | 사업장 ID | 그룹 분할 기준 |
| `asset_id` | 설비 ID | 운영 예측 정렬·추적 |
| `recorded_date` | 관측 날짜 | 날짜별 운영 정책에 사용 |
| `temperature_c` | 온도 | Feature |
| `vibration_mm_s` | 진동 | Feature |
| `alarm_count_7d` | 최근 7일 경보 건수 | Feature |
| `operating_hours` | 누적 작동 시간 | Feature |
| `failure_next_7d` | 관측 뒤 7일 이내 고장 여부(0·1) | Target 전용 |
| `final_repair_cost` | 고장 이후 확정 수리비 | **Feature 사용 금지** |

**`incoming_maintenance.csv`** 는 `failure_next_7d`, `final_repair_cost`가 없는 신규 관측 기록입니다. 신규 입력에는 과거 학습에 존재하지 않았던 `site_id`가 포함될 수 있습니다. `site_id`와 `asset_id`는 모델 입력 Feature로 사용하지 않습니다.

#### 요구사항

1. **입력 검증:** 필수 열 누락, `record_id` 중복, 날짜 오류, 결측값, 비유한 수치를 확인합니다. 네 숫자 Feature 가운데 `vibration_mm_s`, `alarm_count_7d`, `operating_hours`는 음수일 수 없으며 경보 건수는 정수여야 합니다. 무효 행은 `invalid_records.csv`로 분리합니다.
2. **그룹 분할:** 고유 `site_id`를 기준으로 Train 약 60%, Validation 약 20%, Test 약 20%로 나눕니다. `GroupShuffleSplit(random_state=42)`을 이용할 수 있습니다. 사업장 ID의 교집합은 모두 비어 있어야 합니다. 그룹별 행 수가 달라 전체 Sample 비율은 다를 수 있습니다.
3. **Scaling:** 허용된 네 숫자 Feature만 사용합니다. 평균·표준편차는 Training에서 계산하고 Validation·Test·Incoming에 그대로 적용합니다. `final_repair_cost`와 Target을 Feature에 혼합하지 않습니다.
4. **Baseline:**Training 다수 클래스를 예측하는 모델을 기준으로 두고 Test Accuracy·Recall·F2를 함께 기록합니다.
5. **신경망:** `Linear(4,16) → ReLU → Linear(16,8) → ReLU → Linear(8,1)`을 구성합니다. `BCEWithLogitsLoss(pos_weight=...)`의 가중치는 **Training의 음성 수 / 양성 수** 로만 계산합니다. Training에 양성 또는 음성이 하나도 없으면 학습을 중단하고 이유를 기록합니다.
6. **학습:** `AdamW(lr=0.003, weight_decay=0.01)`, Batch Size 32, 최대 80 Epoch를 사용합니다. Validation Loss 기준 Patience 8로 Early Stopping을 수행하고 Best Weight를 복원합니다. 동일한 Seed 42와 CPU 실행을 기본 검증 환경으로 설정합니다.
7. **Threshold 선택:**Validation에서 `[0.25,0.40,0.55,0.70]` 중 F2가 최대인 Threshold를 고릅니다. 동점이라면 더 큰 Threshold를 선택합니다. Test에서 Threshold를 재선택하지 않습니다.
8. **운영 정책:**Incoming에 선택된 Threshold를 적용합니다. Threshold를 통과한 설비 중 **사업장·날짜별 최대 5건** 을 점수 내림차순, 동점이면 `asset_id` 오름차순, 다시 동점이면 `record_id` 오름차순으로 선정합니다. 나머지 기록에는 미선정 사유를 남깁니다.
9. **인계:**Feature 순서·Scaling 기준·Threshold·Best Epoch·Weight를 저장하고, 재로딩 후 동일 Sample의 예측 결과가 일치하는지 확인합니다.

#### 입력 예시

```csv
record_id,site_id,asset_id,recorded_date,temperature_c,vibration_mm_s,alarm_count_7d,operating_hours,failure_next_7d,final_repair_cost
M001,S01,A01,2026-03-01,38,4.1,2,820,0,0
M002,S02,A14,2026-03-01,51,8.2,7,1130,1,230000
```

위 표는 Schema 예시이며, 실제 학습용 파일에는 여러 사업장과 충분한 양성·음성 Sample이 포함됩니다.

#### 출력 파일 규격

- `invalid_records.csv`: `source_file,source_line,record_id,error_code`
- `split_audit.json`: 분할별 Sample·Site 수와 Site ID 교집합 크기
- `training_history.csv`: `epoch,train_loss,validation_loss`
- `evaluation.json`: `best_epoch`, `pos_weight`, `threshold`, Baseline 및 모델의 Test Accuracy·Recall·F2·Confusion Matrix
- `incoming_priorities.csv`: `record_id,site_id,asset_id,recorded_date,probability,selected,status` (`SELECTED`, `BELOW_THRESHOLD`, `CAPACITY_LIMIT`)
- `model_weights.pt`, `preprocessing.json`

평가용 자료에서는 성능 점수가 일률적으로 높게 나오는 것을 강제하지 않습니다. 평가 방식의 독립성과 운영 정책의 정확성이 우선입니다.

#### 검증 항목 (Validation Criteria)

- 중복 Site 없이 분할되었는지, 학습 이후에만 얻을 수 있는 정보를 Feature에서 제외했는지 확인
- `pos_weight`와 Scaling에 Test 또는 Incoming 정보가 섞이지 않았는지 확인
- Best Validation Loss가 발생한 Epoch의 Weight를 선택했는지 확인
- Test 성능과 Incoming 우선 검토 목록을 별도 결과로 보관했는지 확인
- 사업장·날짜별 인원 제한, 동점 규칙, 유효하지 않은 운영 기록의 처리 결과 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 데이터 계약과 그룹 분할:** 유효한 데이터로만 사업장 목록을 구성합니다. GroupShuffleSplit은 그룹 비율을 맞추는 방법이지 각 클래스 분포를 자동으로 보장하는 것은 아닙니다. 각 분할의 클래스 건수를 기록하고 학습 가능성을 검사합니다.

**STEP 2. Model·Loss 구성:**

```python
neg_count = int((train_y == 0).sum())
pos_count = int((train_y == 1).sum())
if neg_count == 0 or pos_count == 0:
    raise ValueError("Training split must contain both classes")

positive_weight = torch.tensor([neg_count / pos_count], dtype=torch.float32)
criterion = torch.nn.BCEWithLogitsLoss(pos_weight=positive_weight)
```

**STEP 3. Early Stopping:**Validation Loss가 엄격하게 개선되면 Best Weight를 깊은 복사로 저장하고 Patience Counter를 초기화합니다. 개선하지 못한 Epoch가 8개 연속되면 중단합니다.

**STEP 4. 평가 및 운영 정책 분리:**Validation으로 결정한 Threshold를 Test와 Incoming에 고정 적용합니다. 성능 평가에는 운영 한도와 별개로 **Threshold 기준 원래 예측** 을 사용하고, 검토 대상 선정 단계에서만 하루 최대 5건 제한을 적용합니다.

</details>

---

### P-02. Microgrid Demand Training — 시간 흐름을 반영한 전력 수요 예측

**관련 개념:** [Chapter 06](../Chapter-06/README.md) · Regression MLP · [Chapter 07](../Chapter-07/README.md) · Temporal Split · Scheduler · Early Stopping · Residual Analysis

#### 문제 설명

지역별 소형 전력망은 다음 날의 전력 수요를 예측하여 공급 계획을 조정합니다. 예측 시점 이후에 확정된 수요를 Feature로 사용하거나 과거와 미래의 날짜를 무작위로 섞으면 실제 운영에서는 얻기 어려운 평가 결과가 나옵니다.

이 과제에서는 미래 정보가 섞이지 않는 날짜 분할, 전력 수요 예측 MLP의 안정적인 학습, Learning Rate Scheduler, 오류 분석과 모델 저장까지 하나의 흐름으로 설계합니다.

#### 제공 데이터

**`microgrid_daily.csv`** 에는 다음 열이 포함됩니다.

```csv
grid_id,date,energy_kwh,temperature_c,weekday,holiday,alarm_count,next_day_energy_kwh
G01,2026-01-01,120,8,3,1,0,127
G02,2026-01-01,96,8,3,1,1,92
G01,2026-01-02,127,7,4,0,0,122
```

- 관측 종료 시점에 이용 가능한 Feature: `energy_kwh`, `temperature_c`, `weekday`, `holiday`, `alarm_count`
- Target: `next_day_energy_kwh` (다음 날 확정되는 값)
- `weekday`는 `0`(월요일)부터 `6`(일요일)까지, `holiday`는 0 또는 1
- `grid_id,date` 조합은 고유해야 합니다. 실제 파일은 날짜별 5개 이상 구역의 기록을 포함합니다.

#### 요구사항

1. **무결성 검사:** 날짜가 올바른 ISO 형식인지, `(grid_id,date)`가 중복되지 않는지, 필수 수치가 유한한지 확인합니다. `energy_kwh`, `alarm_count`, `next_day_energy_kwh`는 음수일 수 없습니다. 유효하지 않은 행은 오류 사유를 포함해 별도로 기록합니다.
2. **Temporal Split:** 정상 기록의 고유 날짜를 오름차순으로 정렬합니다. 첫 60% 날짜는 Train, 다음 20%는 Validation, 마지막 20%는 Test로 나누되 **각 구간 사이의 경계 날짜 1일씩을 Gap으로 제외** 합니다. 이 문서에서는 `floor(0.6D)`, `floor(0.2D)`를 기준으로 날짜 구간을 먼저 나눈 뒤 Train과 Validation의 마지막 날짜를 제외하는 방법으로 통일합니다. `D`는 고유 날짜 수이며, 최소 40일이 제공됩니다.
3. **Baseline:** 관측 당일 `energy_kwh`를 다음 날 수요의 예측값으로 사용하는 Persistence Baseline을 구현합니다.
4. **신경망:** 위 5개 Feature를 입력받는 `Linear(5,24) → ReLU → Linear(24,1)`을 학습합니다. Feature Scaling은 Train에서만 계산합니다. `MSELoss`, `AdamW(lr=0.003)`, Batch Size 32를 사용합니다.
5. **학습 제어:** 최대 120 Epoch 동안 Validation RMSE를 계산하고, `ReduceLROnPlateau(mode="min", factor=0.5, patience=5)`로 학습률을 조정합니다. Early Stopping은 Validation RMSE 기준 Patience 15를 사용하고 Best Weight를 복원합니다.
6. **결과 평가:** 최종 Test에서 Baseline과 MLP의 MAE·RMSE를 계산합니다. 구역별 MAE와 `actual - predicted`인 Residual을 함께 기록하고, 가장 큰 과소 예측 5건을 보고합니다.
7. **모델 전달:**Best Weight, Scaling 기준, 학습 설정, 데이터 분할 날짜를 저장하고, 재로딩된 모델의 추론 결과를 비교합니다.

#### 출력 파일 규격

- `invalid_daily.csv`: `source_line,grid_id,date,error_code`
- `split_dates.json`: Train·Validation·Test 날짜 수와 경계·Gap 날짜
- `training_history.csv`: `epoch,train_mse,validation_rmse,learning_rate`
- `model_comparison.json`: Test Baseline 및 MLP의 `mae,rmse`, `best_epoch`
- `test_predictions.csv`: `grid_id,date,actual,baseline_prediction,model_prediction,residual`
- `grid_report.csv`: `grid_id,sample_count,mae`
- `underprediction_top5.csv`: `grid_id,date,actual,model_prediction,residual`
- `model_weights.pt`, `preprocessing.json`

예측값·오차는 CSV에서 소수점 넷째 자리로 기록하고, 지표 계산은 반올림 이전 값으로 수행합니다.

#### 검증 항목 (Validation Criteria)

- 동일한 날짜의 Sample이 서로 다른 분할에 섞이지 않는지 확인
- Train과 Validation 사이, Validation과 Test 사이에서 Target의 다음 날 정보가 넘어가지 않도록 Gap을 적용했는지 확인
- `scheduler.step(validation_rmse)`가 Validation 측정 후 실행되는지 확인
- Best Model의 Test 점수만 최종 보고하고, Test 지표로 Early Stopping을 조정하지 않는지 확인
- 전력 사용량이 0인 날짜와 과소 예측이 큰 날짜를 올바르게 처리하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 날짜 단위 분할:** `date`의 고유값을 먼저 나눕니다. 예를 들어 구간 경계의 Train 마지막 날짜와 Validation 마지막 날짜를 Gap으로 제외하는 방법을 적용하면 `next_day_energy_kwh` Target의 시간상 중첩을 줄일 수 있습니다.

**STEP 2. Learning Rate 및 Best Weight 관리:**

```python
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode="min", factor=0.5, patience=5
)
# 각 Epoch: 학습 → Validation RMSE 계산 → Best Weight 검사
scheduler.step(validation_rmse)
```

**STEP 3. 실제 운영에 필요한 결과:** 전체 RMSE가 낮아도 특정 구역에서 큰 과소 예측이 반복된다면 운영 위험이 남습니다. `grid_id`별 Residual 분포를 분석하고 Baseline과 비교합니다.

</details>

---

### P-03. Resource-Aware Training Lab — 제한된 자원에서의 학습 설계

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · DataLoader · [Chapter 06](../Chapter-06/README.md) · Parameter Count · [Chapter 07](../Chapter-07/README.md) · Effective Batch · Gradient Accumulation · Clipping · Fair Comparison

#### 문제 설명

학생용 CPU 환경에서 모델을 학습해야 하는 팀은 모델 크기와 학습 예산을 신중하게 선택해야 합니다. 단순히 큰 모델을 만드는 것은 목적이 아닙니다. 동일한 예산에서 학습 시간을 측정하고, Batch Size 제약이 있을 때도 정확한 Gradient를 계산하며, 성능과 자원 사용량을 함께 고려해야 합니다.

본 문제에서는 두 모델 구조와 두 Batch 처리 전략을 비교하고, 제한된 자원에서 학습 가능한 구성을 결정하시오.

#### 제공 데이터

`quality_train.csv`는 다음 형식의 Binary Classification 데이터입니다. 모든 행은 합성 데이터이며, `split`은 `train`, `validation`, `test` 중 하나입니다.

```csv
record_id,split,f1,f2,f3,f4,defective
Q001,train,0.3,12,2.1,5,0
Q002,train,0.8,20,4.3,3,1
Q003,validation,0.5,18,3.1,4,1
Q004,test,0.1,9,1.5,6,0
```

실제 파일은 각 분할에 최소 50개 Sample을 포함하고 Feature는 유한한 수치이며 Target은 0 또는 1입니다.

#### 요구사항

1. **모델 후보:** 구조 S는 `Linear(4,8) → ReLU → Linear(8,1)`, 구조 L은 `Linear(4,32) → ReLU → Linear(32,16) → ReLU → Linear(16,1)`입니다. 각각의 학습 가능한 Parameter 수를 기록합니다.
2. **실험 조건:** `torch.manual_seed(42)`, CPU, `num_workers=0`을 기준으로 합니다. `BCEWithLogitsLoss`와 `AdamW(lr=0.005)`를 사용합니다. Train의 전처리 기준과 분할은 모든 후보가 공유합니다.
3. **업데이트 예산:** 각 후보가 최대 **120회 Optimizer Update** 까지만 수행하도록 합니다. Epoch 수는 데이터셋 크기에 따라 달라질 수 있으며 Update 횟수로 예산을 비교합니다. 같은 후보를 비교할 때는 동일한 초기 Weight와 Sample 순서를 사용합니다.
4. **Effective Batch Size 64:** 방법 A는 가능한 경우 실제 Batch 64를 사용하고, 방법 B는 **Micro-Batch 32개씩 두 번 Gradient를 누적** 합니다. 마지막 묶음이 불완전하면 실제 Sample 수를 이용해 Loss를 가중합니다.
5. **Gradient Clipping:** 각 Optimizer Update 직전, 누적된 Gradient에 `clip_grad_norm_(..., max_norm=1.0)`을 한 번 적용합니다. Micro-Batch마다 개별 Clipping을 수행하지 않습니다.
6. **비교 결과:** 각 구성에서 Validation Accuracy와 Loss, Update 수, Parameter 수, 실제 학습 시간을 기록합니다. 단일 실행 시간만으로 단정하지 않도록 **각 설정 3회 측정값의 중앙값** 을 보고합니다. 측정용 실행에서는 매번 초기 상태를 복원합니다.
7. **모델 선택:**Validation Accuracy가 가장 높은 설정을 선택하고, 동점이면 중앙 실행 시간이 더 짧은 구성을 선택합니다. 중앙값까지 동일하면 구조 S, 그다음 방법 A를 우선합니다. 확정 후 Test Accuracy·F1을 한 번 계산합니다.
8. **관찰 보고:**Micro-Batch 결과가 실제 Batch 방식과 얼마나 다른지 비교합니다. CPU 부동소수점 연산 순서에 따른 작은 차이는 허용하며, 모델 크기와 수행 시간만으로 정확도를 보장하지 않습니다.

#### 출력 파일 규격

- `runs.csv`: `architecture,batch_strategy,run_id,optimizer_updates,validation_loss,validation_accuracy,elapsed_seconds`
- `comparison.csv`: `architecture,batch_strategy,parameter_count,median_seconds,validation_accuracy`
- `selected_model.json`: `architecture,batch_strategy,best_validation_accuracy,test_accuracy,test_f1`
- `gradient_audit.json`: 동일한 초기 Weight·입력에서 실제 Batch와 Micro-Batch로 계산한 Gradient의 최대 절댓값 차이
- `training_report.md`: 실험 조건, 학습 예산, 경계 Batch 처리, 실제 차이의 해석

출력 시간은 실제 CPU에 따라 달라집니다. **특정 초 이하** 를 통과 조건으로 두지 않으며, 빠른 구현이라도 Gradient와 평가 결과가 틀리면 완성으로 간주하지 않습니다.

#### 검증 항목 (Validation Criteria)

- Update 수와 Epoch 수를 혼동하지 않았는지 확인
- Micro-Batch Loss에 `micro_batch_size / accumulated_sample_count` 계수를 적용했는지 확인
- Dataset 크기가 64의 배수가 아니어도 손실 없이 Sample을 처리하는지 확인
- 동일 후보의 반복 실험에서 초기 Weight와 난수 조건을 복원했는지 확인
- Validation의 설정 선택과 최종 Test 평가를 분리했는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. Update 예산 추적:**Epoch를 중간에 끝내더라도 Optimizer Update 횟수가 120을 넘지 않게 합니다. 전체 Sample이 남더라도 Update 예산이 종료되면 해당 실행을 마칩니다.

**STEP 2. Accumulation의 분모:**Effective Batch로 묶은 Micro-Batch의 Sample 수를 먼저 파악하고 각 평균 Loss에 `micro_size / effective_size`를 곱해 역전파합니다. 마지막 묶음도 같은 규칙을 사용합니다.

**STEP 3. Clipping 순서:**

```python
optimizer.zero_grad(set_to_none=True)
for x_micro, y_micro in micro_batches:
    loss = criterion(model(x_micro), y_micro)
    (loss * (len(x_micro) / effective_size)).backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()
```

**STEP 4. 결과 해석:**Clipping을 적용하면 Gradient 원본과 최종 갱신량이 달라집니다. `gradient_audit.json`은 **Clipping 이전 Gradient** 를 비교하도록 해야 연산 일치 여부를 직접 확인할 수 있습니다. 구조별 성능과 속도는 실제 관찰한 값을 토대로 논의합니다.

</details>

---
## Challenge

### C-01. Checkpoint Recovery Investigation — 중단된 학습의 정확한 복구

**관련 개념:** [Chapter 06](../Chapter-06/README.md) · `state_dict` · Dropout · [Chapter 07](../Chapter-07/README.md) · Optimizer State · Scheduler State · RNG · Resume

#### 문제 설명

설비 고장 예측 모델을 20 Epoch 동안 학습하는 과정에서 8번째 Epoch 직후 전원이 차단되었습니다. 담당자는 Weight를 저장했기 때문에 이어서 학습할 수 있다고 판단했지만, 재개한 모델의 결과가 중단 없이 학습한 결과와 달랐습니다.

기존 프로그램은 아래와 같이 Checkpoint를 저장했습니다.

```python
# 기존 코드 일부 — 불완전한 저장 방식
for epoch in range(20):
    train_one_epoch(model, optimizer, train_loader)
    scheduler.step()
    torch.save(model.state_dict(), "checkpoint.pt")

# 재시작 코드 일부
model.load_state_dict(torch.load("checkpoint.pt", weights_only=True))
torch.manual_seed(42)
# Optimizer와 Scheduler를 새로 생성한 상태에서 이어서 학습
```

이 코드는 모델의 Weight만 복원합니다. AdamW의 내부 상태, Scheduler 진행 위치, 난수 생성 상태 및 데이터 순서를 복원하지 않으므로 실제 연속 실행과 다른 Parameter를 얻을 수 있습니다.

**목표는 높은 Accuracy가 아니라, 지정한 조건에서 중단 전후의 학습 결과가 연속 실행과 일치하도록 복구하는 것입니다.**

#### 제공 데이터와 실행 조건

- `train.csv`: `record_id,f1,f2,f3,f4,label` 형식의 실습용 합성 데이터
- `validation.csv`: 동일한 형식의 독립 Validation Data
- Model: `Linear(4,16) → ReLU → Dropout(0.2) → Linear(16,1)`
- Loss: `BCEWithLogitsLoss`, Optimizer: `AdamW(lr=0.005)`, Scheduler: `StepLR(step_size=5,gamma=0.5)`
- Batch Size 16, Epoch 20, CPU, `num_workers=0`
- 데이터 순서는 매 Epoch마다 Shuffle하며, 이를 위해 사용되는 `torch.Generator`의 상태까지 추적합니다.
- 비교용 실행은 동일한 입력 파일과 라이브러리 버전, Thread 설정에서 수행합니다.

#### 요구사항

1. **기준 실행:** 같은 초기 Weight와 Seed를 사용하여 20 Epoch를 중단 없이 학습하고, Epoch별 Training Loss·Validation Loss·Learning Rate를 기록합니다.
2. **중단 실행:** 별도 실행에서 8번째 Epoch까지 동일하게 학습한 뒤 Checkpoint를 저장하고 프로그램을 종료합니다. 중단과 재개는 **Epoch 경계** 에서만 발생하도록 합니다.
3. **상태 보존:** `model_state`, `optimizer_state`, `scheduler_state`, `completed_epoch`, CPU RNG State, DataLoader Shuffle용 Generator State를 저장합니다. Python·NumPy 난수를 실제로 사용했다면 그 상태도 포함합니다.
4. **Early Stopping 상태:** 이번 고정 20 Epoch 비교에서는 중단 조건을 적용하지 않지만, Validation Best Epoch와 Best Weight를 추적한다면 그것도 함께 저장·복원합니다. Best Model과 Resume State는 목적이 다름을 명시합니다.
5. **정확한 재개:**Checkpoint를 불러와 Epoch 9부터 20까지 진행합니다. 새 프로세스에서 Model·Optimizer·Scheduler를 생성한 뒤 각각의 State를 복원하며, 모델 생성에 사용된 난수가 재개 상태에 영향을 주지 않도록 **난수 State는 초기 구성 후 복원** 합니다.
6. **결과 비교:** 연속 실행과 재개 실행의 마지막 Parameter별 최대 절댓값 차이 및 각 Epoch의 Loss·LR 차이를 비교합니다. 같은 CPU·동일한 결정적 실행 조건에서 Parameter 차이는 `1e-6` 이하, LR 차이는 `1e-12` 이하여야 합니다.
7. **안전한 저장:** 새 Checkpoint는 임시 파일에 완성한 뒤 원본 경로로 교체합니다. 쓰기 실패가 발생하더라도 이전 정상 Checkpoint가 남아 있어야 합니다. 파일 손상이 감지되면 불완전한 파일을 학습에 사용하지 않고, 정상 상태를 보존한 채 실패 사유를 보고합니다.
8. **복구 보고서:** 무엇이 잘못되었는지와 수정 전·후 결과의 차이를 정리합니다. 동일한 결과를 얻지 못하는 환경에서는 원인을 보고하고 정확히 일치했다고 주장하지 않습니다.

#### 입력 및 출력

프로그램은 `train.csv`, `validation.csv`와 선택적으로 저장된 `checkpoint.pt`를 사용합니다. 모범 구현은 `continuous`, `interrupt`, `resume`, `compare` 실행 모드를 제공하는 방식으로 구성할 수 있습니다.

- `continuous_history.csv`: `epoch,train_loss,validation_loss,learning_rate`
- `resumed_history.csv`: 같은 열 구조. 1~8 Epoch의 이전 기록과 재개 후 9~20 Epoch 기록을 이어서 보존
- `checkpoint.pt`: 재개에 필요한 학습 상태
- `resume_audit.json`: `completed_epoch`, `resumed_from_epoch`, `max_parameter_diff`, `max_lr_diff`, `matched`
- `recovery_report.md`: 원인 분석, 복구 방식, 손상된 파일 처리 결과

**예상 결과 예시**

```json
{
  "completed_epoch": 20,
  "resumed_from_epoch": 9,
  "max_parameter_diff": 0.0,
  "max_lr_diff": 0.0,
  "matched": true
}
```

위 숫자는 **동일한 결과가 나온 경우의 형식 예시** 이며, 특정 실행에서 관측되었다고 가정한 값이 아닙니다.

#### 검증 항목 (Edge Cases)

- Model Weight만 복원하거나 Scheduler State를 누락했을 때 차이가 발생하는 원인을 설명하는지 확인
- Shuffle과 Dropout의 난수가 정확히 이어지는지 확인
- Epoch 8까지의 기록을 재시작 시 덮어쓰지 않고 보존하는지 확인
- 잘못된 Checkpoint와 쓰기 실패 시 이전 정상 Checkpoint가 유지되는지 확인
- 정확한 Resume와 단순히 Validation 성능이 비슷한 결과를 구분하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 학습 상태를 하나의 구조로 저장:**

```python
checkpoint = {
    "model_state": model.state_dict(),
    "optimizer_state": optimizer.state_dict(),
    "scheduler_state": scheduler.state_dict(),
    "completed_epoch": epoch,
    "torch_rng_state": torch.get_rng_state(),
    "loader_rng_state": loader_generator.get_state(),
}
```

**STEP 2. 저장 원자성:** `torch.save(checkpoint, temp_path)`를 먼저 수행한 뒤 동일 파일 시스템의 목적지에 `os.replace(temp_path, checkpoint_path)`를 사용합니다. 임시 파일 생성과 기존 파일 교체가 실패하는 경우를 별도 테스트합니다.

**STEP 3. 복원 순서:** 새 Model·Optimizer·Scheduler를 구성하고 State를 불러온 뒤 RNG State를 복원합니다. `torch.Generator`를 독립적으로 사용했다면 그 상태도 복원합니다. State 저장 시점과 재개 시점을 일치시켜야 합니다.

**STEP 4. 비교:**

```python
max_diff = max(
    (a - b).abs().max().item()
    for a, b in zip(continuous.parameters(), resumed.parameters())
)
```

비교 대상 두 모델의 Parameter 이름과 Shape도 먼저 일치하는지 검사합니다. 정확한 재현성이 필요한 경우 데이터 읽기 순서와 CPU 연산 환경까지 고정해야 합니다.

</details>

---

### C-02. Inference Incident Response — 운영 중 예측 결과 이상 탐지와 복구

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Dtype · Device · [Chapter 06](../Chapter-06/README.md) · Model Inference · [Chapter 07](../Chapter-07/README.md) · Reproducibility · Model Handoff

#### 문제 설명

공장의 품질 판정 시스템이 기존에는 안정적으로 동작했지만, 입력 CSV를 생성하는 장비가 교체된 뒤 예측 점수가 급격히 달라졌습니다. 현장에서는 일부 행의 측정값이 문자열로 들어오고, Feature 열의 순서도 변경되었습니다. 추론 코드에는 평가 모드를 적용하지 않은 문제도 발견되었습니다.

아래 코드에는 서로 다른 종류의 위험이 섞여 있습니다.

```python
# 기존 코드 일부 — 결함 포함
incoming = pd.read_csv("incoming.csv")
x = torch.tensor(incoming.iloc[:, 1:].to_numpy(), dtype=torch.float32)
model.train()
probabilities = torch.sigmoid(model(x))
probabilities = probabilities.detach().numpy()
```

열 위치를 기준으로 Feature를 구성하여 순서 변경에 취약하고, 학습 시점의 Scaling을 사용하지 않습니다. `train()` 때문에 Dropout이 활성화된 채 추론할 수도 있습니다. 잘못된 숫자 또는 열이 입력되면 Shape·Dtype 문제도 발생합니다.

**목표는 잘못된 예측을 만드는 원인을 특정하고, 추론이 불확실할 때 잘못된 자동 판정을 막는 복구 절차를 구현하는 것입니다.**

#### 제공 파일

- `model_weights.pt`: 신뢰 가능한 기준 모델의 Weight
- `preprocessing.json`: `feature_order`, `mean`, `scale`, `threshold`, `training_min`, `training_max` 저장
- `model_config.json`: 입력 차원, 모델 구조, 출력 차원, 모델 버전
- `reference_cases.csv`: 저장 전 검증된 입력 Sample과 해당 확률 (복구 일치성 검사 전용)
- `incoming.csv`: 운영 중 수신한 신규 데이터. `record_id`와 Feature 열을 포함하지만 **열 순서는 달라질 수 있음**

Feature 이름은 `temperature_c`, `vibration`, `hours_active`로 고정합니다. Training Range의 최소·최대는 Training Data에서 계산된 값이며 Target 정보는 Incoming에 없습니다.

#### 요구사항

1. **정확한 원인 분류:** 열 순서 변경, 숫자 형식 오류, Scaling 누락, `train()` 상태, 잘못된 Model Config를 각각 검증합니다. 재현 로그를 남겨 어떤 문제로 예측이 달라졌는지 구분합니다.
2. **Schema 검사:** `incoming.csv`에 `record_id`와 세 Feature 열이 모두 있어야 합니다. 추가 열은 무시할 수 있으나 필수 열이 하나라도 없으면 전체 추론을 중단하고 `SCHEMA_ERROR`를 보고합니다.
3. **행별 유효성 검사:** `record_id`는 고유한 비어 있지 않은 문자열이어야 합니다. 각 Feature는 유한한 실수이고, `vibration`, `hours_active`는 0 이상입니다. 무효 행은 `INVALID_VALUE`, 유효 ID 중복은 `DUPLICATE_ID`로 분리합니다. 무효 행은 ID를 점유하지 않습니다.
4. **정확한 복원:**Model Config와 Checkpoint의 Parameter Shape를 확인합니다. `torch.load(..., map_location="cpu", weights_only=True)`로 읽고 Feature는 **이름 기준** 으로 정렬합니다. 저장된 Scaling 기준을 적용하고 `eval()` + `torch.inference_mode()`에서 추론합니다.
5. **기준 케이스 비교:** `reference_cases.csv`의 확률과 복원 모델의 확률을 반올림 전 값으로 비교합니다. 최대 차이가 `1e-6`을 넘으면 운영 출력을 차단하고 원인을 보고합니다.
6. **분포 변화 경보:** 신규 유효 행이 30개 이상일 때, 하나 이상의 Feature 값이 **Training Range 밖에 있는 행의 비율** 을 계산합니다. 비율이 20%를 초과하면 `SHIFT_ALERT`를 기록하고 해당 Batch의 자동 확정을 중단합니다. 이 경보는 성능 저하의 증명이 아니라 추가 점검이 필요한 신호입니다.
7. **안전한 출력:**Schema·모델 복원 오류나 기준 케이스 불일치가 발생하면 이전 정상 `predictions.csv`를 덮어쓰지 않습니다. 유효한 추론 결과라도 `SHIFT_ALERT`가 발생하면 점수는 기록하되 상태를 `REVIEW_REQUIRED`로 지정하고 자동 확정은 하지 않습니다.
8. **재현 및 복구 보고:** 정상 입력, 열 순서가 바뀐 입력, 수치 오류, 분포 변화, 잘못된 Model Config를 테스트하고 복구 전·후 차이를 기록합니다.

#### 입력 및 출력 규격

**`incoming.csv`** 예시 (순서가 변경된 경우)

```csv
record_id,hours_active,vibration,temperature_c
I001,220,3.1,34
I002,280,6.2,44
I003,185,unknown,29
```

**`rejected_rows.csv`** 예시

```csv
source_line,record_id,error_code
4,I003,INVALID_VALUE
```

정상 실행에서는 다음 결과를 생성합니다.

- `predictions.csv`: `record_id,probability,predicted,status` (`AUTO` 또는 `REVIEW_REQUIRED`)
- `rejected_rows.csv`: `source_line,record_id,error_code`
- `incident_report.json`: `model_version`, `schema_valid`, `reference_max_abs_diff`, `valid_count`, `invalid_count`, `out_of_range_ratio`, `shift_alert`, `automatic_decisions_enabled`
- `incident_notes.md`: 원인별 재현 과정, 차단·복구 절차, 기준 모델과 결과 비교

입력 상태가 불완전할 때 임의의 0 또는 임의의 예측 Label을 만들어 정상 결과처럼 보고해서는 안 됩니다.

#### 검증 항목 (Validation Criteria)

- 열 순서가 바뀌어도 결과가 같고, 필수 Feature 누락은 정확히 탐지되는지 확인
- Scaling 누락, Mode 설정 오류, Checkpoint Shape 불일치를 서로 구분하는지 확인
- 신규 데이터에 Target이 없어도 Range 기반 경보를 계산할 수 있는지 확인
- `SHIFT_ALERT`가 발생했을 때 기존 점수와 자동 결정 정책을 혼동하지 않는지 확인
- 실패한 실행이 이전의 정상 결과 파일을 손상시키지 않는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 예측 이전에 입력 계약 확인:** 저장된 `feature_order`만을 기준으로 값을 선택합니다. 열이 하나라도 누락되었다면 Shape를 임의로 맞추지 않고 중단합니다.

**STEP 2. 모델 복원과 추론:**

```python
model.load_state_dict(torch.load("model_weights.pt", map_location="cpu", weights_only=True))
model.eval()
with torch.inference_mode():
    logits = model(scaled_inputs)
    probabilities = torch.sigmoid(logits)
```

**STEP 3. 기준 케이스 검증:** 배포할 모델의 동일 입력에 대한 확률을 비교합니다. 통과하지 못하면 실제 Incoming 결과를 생성하기 전에 원인 분석으로 전환합니다.

**STEP 4. 경보와 오류 분리:** 데이터 형식이 잘못된 행은 거부하고, 형식은 유효하지만 Training Range 밖에 있는 행은 분포 변화 계산에 포함합니다. 범위 밖이라는 이유만으로 측정값을 임의로 자르거나 Target을 추정하지 않습니다.

**STEP 5. 결과 교체:** 모든 필수 검사가 끝난 뒤 임시 출력 파일을 완성하고 원자적으로 교체합니다. 차단된 Batch에서는 기존 배포 결과를 유지합니다.

</details>

---
## Radiant

### R-01. The Last Checkpoint — 중단 복구형 모델 학습·추론 플랫폼

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Tensor · Dataset · DataLoader · Autograd · [Chapter 06](../Chapter-06/README.md) · MLP · Binary·Regression Loss · Inference · [Chapter 07](../Chapter-07/README.md) · Optimizer · Scheduler · Early Stopping · Checkpoint · Reproducibility · Gradient Management

#### 문제 설명

여러 지역에 시설을 운영하는 회사는 설비 고장 위험과 다음 날 전력 수요를 예측하는 시스템을 만들었습니다. 모델은 소규모 CPU 서버에서 주기적으로 학습하며, 학습이 끝나면 현장 시스템이 새로운 예측 결과를 사용합니다.

현재 운영에는 세 가지 문제가 있습니다.

첫째, 학습 도중 전원이 끊어지면 처음부터 다시 실행해야 합니다. 둘째, 최신 모델을 배포한 직후 예측 결과가 달라져도 어떤 데이터와 Weight로 생성한 결과인지 추적하기 어렵습니다. 셋째, 새 모델의 점수가 좋아 보인다는 이유로 기존 모델을 교체했지만, 일부 사업장에서는 잘못된 경보가 더 많이 발생했습니다.

이번 과제의 목표는 **높은 점수를 내는 신경망 하나를 만드는 것이 아니라, 신뢰할 수 있는 모델을 학습·검증·전달하고 문제가 발생하면 이전 정상 상태로 돌아갈 수 있는 체계를 완성하는 것** 입니다.

다음 기능을 하나의 재현 가능한 Python 프로젝트로 설계하시오.

- 설비 고장 위험 Binary Classification
- 다음 날 전력 수요 Regression
- 중단된 학습의 정확한 재개
- 신규 사업장과 미래 데이터의 독립 평가
- 검증된 새 모델의 안전한 배포·복구
- 실시간 입력 오류와 분포 변화 감지
- Batch 추론의 처리 효율 분석

이 과제는 Chapter 05~07에서 배운 PyTorch만으로 구현할 수 있어야 합니다. CNN, Transformer, 분산 학습과 외부 클라우드 서비스는 요구하지 않습니다.

#### 제공 데이터와 시점

모든 파일은 UTF-8 형식이고, 데이터는 실습용 합성 데이터입니다. 실제 시설이나 개인에 관한 데이터는 포함하지 않습니다.

**1. `sites.csv` — 시설 기준 정보**

```csv
site_id,zone,capacity
S001,NORTH,200
S002,SOUTH,150
```

- `site_id`: 시설 고유 식별자
- `zone`: 운영 지역
- `capacity`: 1 이상의 정수, 모델 입력 Feature

**2. `history.csv` — 과거 관측값 및 사후 확정 Target**

```csv
site_id,date,temperature_c,vibration,energy_kwh,alarms_7d,failure_next_7d,energy_next_day,final_repair_cost
S001,2026-06-01,23,2.1,96,1,0,102,0
S002,2026-06-01,25,4.3,84,3,1,91,150000
```

| 열 | 의미 | 사용 기준 |
|---|---|---|
| `site_id`, `date` | 시설과 관측 날짜 | 연결·분할·중복 판단 |
| `temperature_c` | 당일 관측 기온 | Feature |
| `vibration` | 당일 진동 값 | Feature, 0 이상 |
| `energy_kwh` | 당일 전력 사용량 | Feature, 0 이상 |
| `alarms_7d` | 관측 시점까지 최근 7일 경보 수 | Feature, 0 이상의 정수 |
| `capacity` | `sites.csv`에서 결합한 시설 수용 규모 | Feature |
| `failure_next_7d` | 관측 이후 7일 동안 고장이 발생했는지 여부 | Classification Target 전용 |
| `energy_next_day` | 관측 다음 날의 확정 전력 수요 | Regression Target 전용 |
| `final_repair_cost` | 정비 후 확정된 수리비 | **Feature 사용 금지** |

**3. `incoming.csv` — 운영 추론 대상**

```csv
site_id,date,temperature_c,vibration,energy_kwh,alarms_7d
S001,2026-09-01,24,2.4,105,1
S002,2026-09-01,26,4.7,89,4
```

Incoming 데이터에는 Target과 `final_repair_cost`가 없습니다. 관측이 끝난 시점에 다음 날 전력 수요와 이후 7일의 고장 위험을 예측합니다.

**4. `deployment_manifest.json` — 현재 배포 중인 모델 정보**

첫 실행 시에는 배포된 모델이 없는 상태입니다.

```json
{
  "active_version": null,
  "status": "EMPTY"
}
```

프로젝트는 최소 10개 시설과 아래 날짜 구간마다 충분한 기록이 있는 데이터를 대상으로 합니다. Training·Validation에는 두 클래스가 모두 존재하도록 실습 데이터가 구성됩니다. Incoming은 최소 30개 이상의 유효한 시설·날짜 기록을 제공하는 기본 검증 세트를 포함합니다.

#### 데이터 무결성과 처리 규칙

1. 모든 CSV는 헤더를 포함합니다. `sites.csv`의 `site_id`는 고유해야 하며 `capacity`가 1 이상의 정수여야 합니다. 시설 기준 파일의 오류는 전체 처리 중단 사유입니다.
2. 과거·운영 데이터의 키는 `(site_id,date)`입니다. 등록되지 않은 시설은 `UNKNOWN_SITE`, 잘못된 날짜는 `INVALID_DATE`, 누락 또는 비유한 숫자와 범위 오류는 `INVALID_VALUE`, 잘못된 Target은 `INVALID_TARGET`으로 기록합니다.
3. 동일한 키를 가진 여러 기록 가운데 **첫 번째 유효한 행만 인정** 합니다. 유효한 중복 기록은 `DUPLICATE_RECORD`로 거부합니다. 앞선 무효 행은 키를 점유하지 않습니다.
4. 오류 판정 우선순위는 `UNKNOWN_SITE` → `INVALID_DATE` → `INVALID_VALUE` → `INVALID_TARGET` → `DUPLICATE_RECORD`입니다. Incoming에는 Target이 없으므로 `INVALID_TARGET` 검사를 적용하지 않습니다.
5. `temperature_c`는 음수를 허용하지만 유한한 실수여야 합니다. `vibration`·`energy_kwh`는 0 이상, `alarms_7d`는 0 이상의 정수입니다. `failure_next_7d`는 0 또는 1, `energy_next_day`는 0 이상의 유한 실수입니다.
6. 정합성 검사를 통과한 기록은 날짜 오름차순, 같은 날짜에서는 시설 ID 오름차순으로 정렬합니다. 모든 오류 기록에는 `source_file`, 실제 파일 행 번호 `source_line`, `error_code`를 포함합니다.
7. `final_repair_cost`는 사후 정보이므로 수치가 입력되어 있더라도 예측 Feature, Scaling 기준 및 모델 선택 기준에 사용하지 않습니다.

#### 요구사항

**STEP 01 — 데이터 준비와 검증**

- 세 CSV를 검사하고 정상 행과 거부 행을 분리합니다.
- Training에서 사용할 Feature 목록을 `[temperature_c, vibration, energy_kwh, alarms_7d, capacity]`로 고정합니다.
- 모든 Feature의 Scaling 기준은 Training 데이터에서만 계산합니다. 표준편차가 0인 Feature는 Scale을 1로 처리합니다.
- 정상·오류 행의 개수, 시설 수, 날짜 범위와 오류 코드별 건수를 기록합니다.
- 데이터 검증에 실패해 학습할 수 없다면 이전에 배포한 모델과 결과를 손상시키지 않습니다.

**STEP 02 — 시간 구간과 신규 시설 분리**

날짜 기준은 다음과 같이 고정합니다.

| 구간 | 기록 날짜 | 용도 |
|---|---|---|
| Training | 2026-03-01 ~ 2026-06-30 | 학습·전처리 기준 |
| Gap 1 | 2026-07-01 ~ 2026-07-07 | 평가 대상에서 제외 |
| Validation | 2026-07-08 ~ 2026-07-21 | Best Weight·Threshold·배포 후보 비교 |
| Gap 2 | 2026-07-22 ~ 2026-07-28 | 평가 대상에서 제외 |
| Test | 2026-07-29 ~ 2026-08-11 | 독립적인 최종 평가 |

고장 여부가 관측 이후 7일의 사건을 Target으로 사용하므로 구간 사이에 7일의 Gap을 둡니다. Gap은 학습·모델 선택·점수 계산에 포함하지 않습니다. 운영 추론 날짜는 `2026-09-01` 이후이며, Test Target이 확정된 뒤에 배포 평가가 진행된다고 가정합니다.

추가로 학습하지 않은 시설에 대한 일반화 성능도 평가합니다.

- 고유 `site_id`를 문자열 오름차순으로 정렬한 뒤 **5번째, 10번째, 15번째 …** 시설을 Holdout으로 지정합니다.
- Holdout 시설의 모든 기록은 Training·Validation과 Scaling에 사용하지 않습니다.
- **평가 A:**Holdout이 아닌 시설의 Test 기간 기록
- **평가 B:**Holdout 시설의 Test 기간 기록

평가 A와 B의 결과를 따로 기록합니다. Holdout 시설의 Target을 사용해 모델·Threshold·배포 후보를 선택하지 않습니다.

**STEP 03 — 두 종류의 MLP 구성 및 학습**

Classification과 Regression을 서로 독립적인 모델로 구성합니다. 공통 입력은 5개 Feature입니다.

| 구분 | Model 구조 | Loss | 주요 Metric |
|---|---|---|---|
| Classification | `Linear(5,16) → ReLU → Linear(16,1)` | `BCEWithLogitsLoss` | Recall, F2, Precision |
| Regression | `Linear(5,16) → ReLU → Linear(16,1)` | `MSELoss` | MAE, RMSE |

- 두 모델 모두 Dataset·DataLoader를 사용하고 CPU 실행을 기본으로 합니다.
- 1개 Batch는 최대 32개 Sample을 포함하고 마지막 Batch를 버리지 않습니다.
- Training Loss는 Batch별 단순 평균이 아니라 Sample 수를 반영해 집계합니다.
- Gradient 초기화는 매 Optimizer Update 전에 수행합니다.
- Classification의 Baseline은 Training 다수 클래스를 예측하는 모델이며, Regression Baseline은 당일 `energy_kwh`를 그대로 예측하는 방법입니다.

**STEP 04 — 배포 버전별 학습과 중단 복구**

모델 버전을 두 단계로 구성합니다.

- **v1:** `SGD(lr=0.02, momentum=0.9)`, 최대 24 Epoch
- **v2:** `AdamW(lr=0.005, weight_decay=0.01)`, 최대 24 Epoch

두 버전은 같은 Model 구조와 초기 Seed 42, DataLoader 순서, Training·Validation 데이터로 시작합니다. 단, Optimizer 설정이 다르므로 같은 학습 궤적이나 같은 성능을 기대하는 것은 아닙니다.

v2 학습에는 `StepLR(step_size=8,gamma=0.5)`를 적용합니다. Validation Metric이 개선된 Best Weight를 보관하고 Early Stopping Patience 6을 적용하되, **최소 8 Epoch를 완료한 뒤부터** 중단 조건을 허용합니다. v1·v2의 최고 Validation 기준은 Classification에서는 F2, Regression에서는 RMSE입니다. Classification Threshold는 Validation에서 `[0.30,0.50,0.70]` 중 F2가 가장 높은 값을 고르고, 동점은 더 높은 Threshold를 선택합니다.

v2는 **6번째 Epoch 종료 직후 의도적으로 중단하고 새 프로세스에서 재개** 해야 합니다. Checkpoint에는 최소한 다음 상태가 포함되어야 합니다.

- Model·Optimizer·Scheduler State
- 완료한 Epoch, Best Validation Metric·Best Weight, Early Stopping Counter
- Torch RNG State와 Shuffle용 Generator State
- 학습에 영향을 준 Config·Feature 순서·Scaling 기준의 식별 정보

연속 실행과 중단·재개 실행을 동일한 CPU·입력·환경에서 비교하여 최종 Parameter의 최대 절댓값 차이가 `1e-6` 이하인지 검사합니다. 저장은 임시 파일 작성 후 원자적 교체를 사용합니다.

**STEP 05 — Validation 기반 배포 후보 선택**

v1과 v2를 **Validation에서만** 비교합니다. 배포 승격 규칙을 다음과 같이 고정합니다.

1. v2의 Classification Validation F2가 v1보다 낮아서는 안 됩니다.
2. v2의 Regression Validation RMSE가 v1보다 높아서는 안 됩니다.
3. 두 조건을 충족하며 적어도 하나의 지표가 엄격하게 개선되어야 v2를 승격합니다.
4. 이 조건을 만족하지 않으면 v1을 유지합니다.

비교는 반올림 전 값으로 수행합니다. 선정이 끝나면 **확정한 버전의 두 모델** 로만 평가 A·B의 Test 점수를 계산합니다. Test 성능을 보고 승격 결정을 바꾸지 않습니다.

**STEP 06 — 운영 추론과 경보 처리**

- `incoming.csv`의 Feature를 저장된 이름·순서와 Scaling 기준으로 변환합니다.
- `eval()`과 `torch.inference_mode()`에서 Classification 확률과 Regression 예측값을 계산합니다.
- Classification의 확률이 선정된 Threshold 이상인 기록을 점검 후보로 정합니다.
- **지역(`zone`)·날짜별 최대 3개 시설** 을 확률 내림차순, 동점 시 시설 ID 오름차순으로 선정합니다. 나머지는 `BELOW_THRESHOLD` 또는 `CAPACITY_LIMIT`로 표시합니다.
- 신규 입력에서 한 행이라도 누락값이나 범위 오류가 있으면 해당 행을 거부하며, 유효한 나머지 기록은 별도로 처리합니다.

**STEP 07 — 분포 변화 경보와 안전한 배포**

- Training에서 Feature별 관측 최소·최댓값을 함께 저장합니다.
- Incoming에서 유효 행이 30개 이상이면, 하나 이상의 Feature가 Training Range 밖에 있는 행의 비율을 구합니다.
- 해당 비율이 20%를 초과하면 `SHIFT_ALERT`를 기록하고 자동 점검 대상 확정을 중단합니다. 예측 점수는 확인용으로 남길 수 있지만 `REVIEW_REQUIRED`로 구분합니다.
- 새 모델의 학습·검증과 Incoming 추론을 모두 통과한 뒤에만 배포 버전 정보를 갱신합니다. 배포 정보 파일은 마지막에 교체합니다.
- 모델 파일 손상, Loader 예외, 기준 예측값 불일치 또는 결과 저장 실패가 발생하면 이전 정상 버전의 Weight·전처리 기준·결과를 유지해야 합니다.
- 배포 이후 문제가 확인되면 이전 정상 버전으로 Rollback할 수 있어야 합니다. 배포 버전의 변경 이력을 기록합니다.

**STEP 08 — 추론 최적화 및 결과 일치 검증**

- 검증 가능한 기준 구현(행별 추론)과 Batch 단위 Tensor 추론을 각각 실행합니다.
- 동일한 입력에 대해 Classification 확률과 Regression 예측값의 최대 절댓값 차이가 `1e-6` 이하인지 확인합니다.
- 동일 CPU에서 여러 번 실행한 처리 시간을 측정하고 중앙값을 기록합니다. 환경에 따라 시간 차이가 달라지므로 특정 속도 향상을 요구하지 않습니다.
- 추론 속도가 개선되어도 행 순서, 예측값, 상태 코드, 경보 목록이 바뀌지 않아야 합니다.

#### 입력 및 출력 규격

프로젝트의 기본 실행은 `validate`, `train`, `resume`, `evaluate`, `predict`, `promote`, `rollback`, `benchmark`처럼 단계별 명령으로 분리할 수 있습니다. 내부 코드 구조는 자유롭지만 각 단계는 이전 단계의 산출물에 의존하는 조건을 명확히 검사해야 합니다.

**필수 결과물**

| 파일 | 내용 |
|---|---|
| `clean_history.csv` | 정상 과거 기록, 날짜·시설 ID 정렬 |
| `rejected_rows.csv` | `source_file,source_line,error_code` |
| `data_audit.json` | 유효·무효 행 수, 오류 코드, 분할 날짜, Holdout Site 목록 |
| `training_history.csv` | `version,task,epoch,train_loss,validation_metric,learning_rate` |
| `checkpoints/` | v2의 중단·재개 학습 상태, Best Weight |
| `resume_audit.json` | 연속 실행과 재개 실행의 Parameter 차이, 성공 여부 |
| `validation_selection.json` | v1·v2 Validation 지표와 배포 후보 선택 이유 |
| `test_evaluation.json` | 평가 A·B의 Classification·Regression 지표와 Baseline 비교 |
| `deployment_manifest.json` | 현재 버전, Model·전처리 파일 경로, 검증 상태 |
| `incoming_predictions.csv` | `site_id,date,failure_probability,energy_prediction,selected,status` |
| `shift_report.json` | 유효 행 수, 범위 초과 비율, `SHIFT_ALERT`, 자동 확정 가능 여부 |
| `benchmark.json` | 행별·Batch 추론 시간 중앙값, 결과 최대 차이 |
| `final_report.md` | 실험 설계, 복구·배포 이력, Test 평가, 오류 분석 및 성능 비교 |

Classification 평가에는 Accuracy만 제시하지 말고 Precision·Recall·F2·Confusion Matrix를 포함해야 합니다. Regression에는 MAE와 RMSE를 함께 기록하며, Test 예측값의 오차가 큰 사례도 분석합니다. 수치 파일은 소수점 넷째 자리로 기록해도 되지만 모든 비교와 경보 판정은 반올림 전 값으로 수행합니다.

#### 공개 검증 예제 — 무효 행과 중복 처리

다음은 Schema 검사 후 정상 행 선택 규칙만 보여 주는 예시입니다. 전체 모델을 학습하기 위한 데이터 규모가 아닙니다.

**`sites.csv`**

```csv
site_id,zone,capacity
S001,NORTH,200
S002,SOUTH,150
```

**`history.csv`**

```csv
site_id,date,temperature_c,vibration,energy_kwh,alarms_7d,failure_next_7d,energy_next_day,final_repair_cost
S001,2026-06-01,23,2.1,96,1,0,102,0
S001,2026-06-01,24,2.2,98,2,0,105,0
S002,2026-06-01,25,-1,84,3,1,91,150000
S002,2026-06-01,25,4.3,84,3,1,91,150000
```

**예제 `rejected_rows.csv`**

```csv
source_file,source_line,error_code
history.csv,3,DUPLICATE_RECORD
history.csv,4,INVALID_VALUE
```

`S001`의 첫 번째 유효 기록만 인정합니다. `S002`의 음수 진동 기록은 무효이므로 같은 키를 점유하지 않고, 그 다음 유효 기록을 정상 처리합니다.

#### 최종 검증 항목

1. **구조와 수식:**Tensor Shape, Logit·Target Shape, Loss와 Training Loop가 의도한 대로 작동하는지 확인
2. **데이터 무결성:** 무효 행이 학습·평가·운영 출력에 섞이지 않고 오류 사유를 추적할 수 있는지 확인
3. **미래 정보 차단:** 사후 수리비와 미래 Target이 Feature에 들어가지 않으며, 날짜 Gap과 Holdout 구분이 지켜지는지 확인
4. **정확한 복구:**Optimizer·Scheduler·난수 상태를 포함한 Resume이 연속 실행 결과와 일치하는지 확인
5. **독립적인 평가:**Validation으로 확정한 모델·Threshold를 Test에서 변경하지 않는지 확인
6. **안전한 운영 정책:** 지역별 점검 한도, 동점 처리, Shift 경보와 자동 처리 차단이 정확한지 확인
7. **배포·복구:** 새 버전 실패 시 이전 정상 Weight·전처리·결과가 남고 Rollback이 가능한지 확인
8. **재현성:** 동일한 입력·설정에서 파일 순서와 결정적 판단 결과가 일치하는지 확인
9. **최적화:** 더 빠른 추론 구현이 결과를 바꾸지 않으며, 시간 측정 조건을 명확히 기록했는지 확인

#### 제출 결과물

실행 가능한 Python 프로그램, 실습용 합성 데이터, 결과 파일, 자동 검증 코드와 최종 보고서를 제출합니다. 코드의 폴더 구조는 자유롭게 설계할 수 있으나, 데이터 검사부터 학습·복구·평가·배포·Rollback까지 각 단계의 입력과 출력이 명확해야 합니다.

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 데이터 계약 확정:** 학습 코드를 작성하기 전에 필수 열, 허용 범위, 분할 날짜와 오류 코드를 정의합니다. 행별 검증이 완료되면 모델은 정상 배열만 입력받도록 구성합니다.

**STEP 2. Baseline 및 두 Task 분리:**Classification과 Regression의 모델·Loss·Optimizer 상태를 독립적으로 관리합니다. 전처리는 같은 Training 행에서 계산한 기준을 공유할 수 있지만, Target과 평가 지표는 섞지 않습니다.

**STEP 3. 학습 모듈 구성:**Model 생성, `train_epoch`, `evaluate`, Best Weight 선택, Scheduler Step, Checkpoint 저장·복원을 기능별로 분리합니다. Training Loss에는 Sample 수 가중 평균을 적용합니다.

**STEP 4. Resume 검증 선행:** 중단·재개 비교에서 차이가 있으면 새 버전을 배포 후보로 등록하지 않습니다. 특히 난수 복원 시점과 Shuffle Generator State를 점검합니다.

**STEP 5. 배포 후보와 Test 분리:**Validation에서 v1·v2의 성능 비교를 끝낸 뒤 모델을 확정합니다. Test는 확정한 버전의 보고용 점수에만 사용합니다.

**STEP 6. 추론의 입력 계약 고정:**Feature 순서·Scaling 기준·Model State가 하나의 배포 버전에 연결되어야 합니다. `eval()`과 `inference_mode()`를 명시적으로 적용합니다.

**STEP 7. 원자적 결과 교체:** 결과를 임시 작업 디렉터리에 전부 생성해 검사한 뒤, 신규 배포 버전을 등록합니다. 단순히 각 파일을 순서대로 덮어쓰면 중간 실패 시 서로 다른 버전의 파일이 섞일 수 있습니다. 버전 디렉터리를 별도로 보관하고 **Manifest를 마지막에 교체** 하는 구조가 안전합니다.

**STEP 8. 경보 정책과 최적화:** 분포 변화 경보는 실제 오분류 여부와 별개입니다. 자동 처리 여부를 먼저 결정하고, 성능 최적화는 정상 작동하는 기준 구현과 결과가 같음을 확인한 뒤 진행합니다.

</details>

---

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)
