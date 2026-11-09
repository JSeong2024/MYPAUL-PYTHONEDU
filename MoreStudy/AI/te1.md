# Problems — Summary Part 02

Chapter 05~07 · **Basic 5 · Advanced 4 · Professional 3 · Challenge 2 · Radiant 1**

각 문제의 입력·출력 조건을 충족하는 Python 프로그램을 작성하시오.

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)

## Basic

### B-01. 텐서 구조와 차원별 집계

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Tensor · Shape · Dtype · Reduction

#### 문제 설명

센서에서 수집한 측정값이 행렬 형태로 주어집니다. 데이터를 Tensor(텐서)로 변환하여 채널별 합계와 Sample(샘플)별 평균을 계산하십시오. 텐서의 Shape와 자료형도 함께 출력하십시오.

#### 요구사항

1. 입력에서 샘플 수 `N`과 채널 수 `D`를 읽고 Shape `(N, D)`의 텐서를 생성한다.
2. 채널별 합계는 `dim=0`, 샘플별 평균은 `dim=1`로 계산한다.
3. 수치는 소수점 둘째 자리까지 표시한다.
4. 행·열 개수나 숫자 형식이 잘못되었거나 유한하지 않은 값이 있으면 `INVALID`만 출력한다.

#### 입력

첫 줄에는 `N D`가 주어집니다. 이후 `N`개 줄에는 각각 `D`개의 실수가 공백으로 구분되어 주어집니다.

- `1 ≤ N ≤ 200`, `1 ≤ D ≤ 20`
- `3`처럼 소수점 없이 표기된 값도 실수형으로 처리합니다.
- `NaN`, 무한대 및 추가 데이터 행은 허용하지 않습니다. 입력값은 `float32`에서 유한하게 표현할 수 있는 범위에 속합니다.

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

#### 검증 기준

- `N=1`, `D=1`에서 차원이 사라지지 않는지 확인
- 누락·초과된 원소와 잘못된 숫자를 구분 없이 `INVALID`로 처리하는지 확인
- 합계와 평균이 올바른 차원에 대해 계산되는지 확인


---

### B-02. 센서 측정값 보정

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Broadcasting · Element-wise Operations · Reduction

#### 문제 설명

여러 센서 채널에서 수집한 측정값이 행렬로 주어집니다. 채널마다 보정값과 배율이 다르므로 Tensor(텐서)의 Broadcasting을 이용해야 합니다. 아래 식에 따라 측정값을 보정하고 채널별 평균을 출력하십시오.

```math
z_{ij}=(x_{ij}+o_j)s_j
```

- $x_{ij}$: $i$번째 Sample(샘플)의 $j$번째 채널 측정값
- $o_{j}$: 채널 $j$의 Offset
- $s_{j}$: 채널 $j$의 Scale

#### 요구사항

1. 측정값 행렬의 Shape는 `(N, D)`, Offset과 Scale의 Shape는 `(D,)`로 구성한다.
2. Broadcasting으로 전체 행렬을 한 번에 보정한다.
3. 보정된 샘플을 원래 순서대로 출력하고, 채널별 보정 평균을 계산한다.
4. Offset·Scale의 길이가 맞지 않거나 Scale이 0 이하이면 `INVALID`를 출력한다.

#### 입력

첫 줄에 `N D`, 두 번째 줄에 `D`개의 Offset, 세 번째 줄에 `D`개의 Scale이 주어집니다. 이어서 `N`개 측정값 행이 주어집니다.

- `1 ≤ N ≤ 200`, `1 ≤ D ≤ 20`
- 모든 입력값은 유한한 실수이며, Scale은 모두 양수입니다.

#### 출력

각 보정 결과 행은 `SAMPLE_i`로, 채널별 평균 행은 `CHANNEL_MEAN`으로 시작합니다. 모든 수치는 소수점 둘째 자리까지 표시합니다.

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

#### 검증 기준

- Offset과 Scale을 샘플 축이 아닌 채널 축에 적용했는지 확인
- 단일 샘플 또는 단일 채널에서도 Broadcasting이 올바르게 동작하는지 확인
- Shape 불일치, 0 이하의 Scale, 무한대 입력을 올바르게 처리하는지 확인


---

### B-03. Autograd를 이용한 Gradient 계산

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Autograd · Gradient · [Chapter 06](../Chapter-06/README.md) · Loss

#### 문제 설명

선형 Model(모델) `wx+b`로 입력 `x`의 예측값을 구하고, 정답 `y`와의 오차를 계산합니다. Autograd로 Gradient를 계산해 Parameter(파라미터)를 한 번 갱신하십시오. 갱신 전의 예측값·Loss·Gradient와 갱신한 파라미터·예측값을 지정된 형식으로 출력하십시오. 여러 Epoch에 걸친 학습은 수행하지 않습니다.

```math
\hat y=wx+b,\quad L=(\hat y-y)^2
```

```math
w_{\mathrm{new}}=w-\eta\frac{\partial L}{\partial w},\quad
b_{\mathrm{new}}=b-\eta\frac{\partial L}{\partial b}
```

#### 요구사항

1. `w`, `b`를 `requires_grad=True`인 Scalar Tensor(텐서)로 생성한다.
2. 예측값과 Loss를 계산한 뒤 `backward()`를 한 번 호출한다.
3. `w.grad`와 `b.grad`를 출력한다.
4. `torch.no_grad()` 문맥에서 파라미터를 한 번 갱신한 뒤 새 예측값을 출력한다.
5. 갱신 전의 Gradient와 Loss를 별도로 보관하여 처음 계산한 값을 출력한다.

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

#### 검증 기준

- `x=0`일 때 Weight Gradient가 0이 되는지 확인
- 예측이 정확하여 Loss가 0인 경우 Gradient도 0인지 확인
- `backward()`를 중복 호출해 Gradient를 누적하지 않는지 확인


---

### B-04. 신경망 구조와 파라미터 수

**관련 개념:** [Chapter 06](../Chapter-06/README.md) · `nn.Linear` · ReLU · Parameter Count · Forward

#### 문제 설명

입력 Feature(특성) 수, 은닉 뉴런 수, 출력 뉴런 수가 주어집니다. 이를 이용해 `Linear → ReLU → Linear` 구조의 MLP를 구성하십시오. 학습은 수행하지 않으며, Forward 결과의 Shape와 학습 가능한 Parameter(파라미터) 수를 출력하십시오.

#### 요구사항

1. `nn.Sequential(nn.Linear(D, H), nn.ReLU(), nn.Linear(H, O))`를 구성한다. 두 Linear Layer 모두 Bias를 사용한다.
2. 첫 Layer와 두 번째 Layer의 파라미터 수를 구한다.
3. Batch Size가 `N`인 영(0) Tensor(텐서)를 입력하여 Forward 결과의 Shape를 확인한다.
4. 입력 범위가 잘못되면 `INVALID`를 출력한다.

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

#### 검증 기준

- Bias를 빠뜨리지 않고 계산하는지 확인
- `nn.Linear`의 Weight Shape가 `(out_features, in_features)`임을 반영했는지 확인
- 출력 Shape를 실제 Forward 실행으로 검사하는지 확인


---

### B-05. DataLoader의 배치 구성

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · TensorDataset · DataLoader · Batch Size · `drop_last`

#### 문제 설명

Sample(샘플) ID 목록과 배치 크기가 주어집니다. `DataLoader`를 이용해 ID를 입력 순서대로 배치에 나누어 담고, 각 배치의 구성과 제외된 샘플 수를 출력하십시오.

#### 요구사항

1. 입력된 ID를 `torch.long` Tensor(텐서)로 만든 뒤 `TensorDataset`과 `DataLoader`를 사용한다.
2. `shuffle=False`, 지정된 `batch_size=B`, 지정된 `drop_last` 옵션을 적용한다.
3. 생성된 Batch 개수, 각 Batch의 ID 목록, 사용하지 않은 샘플 수를 출력한다.
4. 입력에 오류가 있으면 `INVALID`를 출력한다.

#### 입력

첫 줄에 `N B drop_last`가 주어지고, 다음 줄에는 서로 다른 정수형 ID `N`개가 주어집니다.

- `1 ≤ N ≤ 200`, `1 ≤ B ≤ 200`
- `drop_last`는 `0` 또는 `1`입니다.

#### 출력

`drop_last=1`이면 크기가 `B`보다 작은 마지막 Batch를 제외합니다.

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

#### 검증 기준

- `N`이 `B`로 나누어떨어지지 않는 경우
- `B > N`이면서 `drop_last=1`인 경우 (`BATCHES 0`)
- 중복 ID, 잘못된 Flag, 부족하거나 초과된 입력값


---

## Advanced

### A-01. 센서 데이터 품질 검사와 보정

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Tensor · Broadcasting · Mask · Data Validation

#### 문제 설명

시설 운영 시스템은 공간별 온도·습도·전력 사용량을 수집합니다. 센서마다 보정값이 다르고, 일부 기록에는 누락값이나 허용 범위를 벗어난 값이 포함되어 있습니다. 이런 기록까지 집계하면 평균이 왜곡될 수 있으므로 데이터 검증이 먼저 필요합니다.

두 CSV를 읽어 유효한 기록만 Tensor(텐서)로 구성한 뒤, 채널별 보정과 집계 결과를 파일로 저장하는 프로그램을 작성하십시오.

#### 요구사항

1. `sensor_readings.csv`의 필수 열과 값의 유효성을 검사한다. `record_id`는 공백이 없는 고유 문자열이어야 하며, `room_id`는 비어 있으면 안 된다.
2. 측정값의 허용 범위는 `-40 ≤ temperature ≤ 100`, `0 ≤ humidity ≤ 100`, `power_kw ≥ 0`이다. 값은 모두 유한한 실수여야 한다.
3. 오류 우선순위는 **필수값 누락 → 잘못된 숫자 또는 범위 → 유효한 ID 중복** 순서로 정한다. 무효 행은 ID를 점유하지 않는다.
4. `calibration.csv`에서 세 Feature(특성)의 Offset과 Scale을 읽는다. 특성은 `temperature`, `humidity`, `power_kw`가 정확히 한 번씩 있어야 하며 Scale은 양수이다. 보정식은 `z=(x+offset)*scale`이다.
5. 정상 측정값을 Shape `(N, 3)`의 `float32` 텐서로 변환하고 Broadcasting으로 보정한다.
6. `calibrated.csv`, `rejected_rows.csv`, `quality_report.json`을 생성한다. 정상 Sample(샘플)이 5개 미만이면 `calibrated.csv`를 생성하지 않고 부족한 샘플 수를 `quality_report.json`에 기록한 뒤 실패 상태로 종료한다. `rejected_rows.csv`와 `quality_report.json`은 그대로 생성한다.

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

*위 두 파일은 데이터 형식 예시입니다. 실제 프로젝트 데이터에는 정상 기록이 5개 이상 포함됩니다.*

#### 출력 파일 규격

- `calibrated.csv`: `record_id,room_id,temperature,humidity,power_kw` 순서. 정상 행은 원본 순서 유지, 실수는 소수점 넷째 자리까지 기록
- `rejected_rows.csv`: `source_line,record_id,error_code` 순서. 헤더를 1행으로 세어 입력 행 번호를 기록. 코드는 `MISSING_VALUE`, `INVALID_NUMBER`, `DUPLICATE_ID`
- `quality_report.json`: `status`, `valid_count`, `rejected_count`, `shape`, `channel_mean`의 다섯 항목. 정상 처리 시 `status`는 `OK`, 샘플이 부족하면 `INSUFFICIENT_DATA`로 기록. `shape`는 `[N,3]`. 정상 샘플이 없으면 `channel_mean`은 `null`, 그 외에는 세 특성의 보정 평균을 기록

**예제 처리 결과**

`R01`의 보정값은 `[21,45,6]`, `R02`는 `[23,50,8]`입니다. `R03`은 온도 누락으로 거부됩니다. 이 예시에는 정상 기록이 2개뿐이므로 `calibrated.csv`를 생성하지 않고, `quality_report.json`에 샘플 부족 상태를 기록해야 합니다.

#### 검증 기준

- 정상 행 이전에 등장한 무효 ID가 이후 정상 행을 잘못 차단하지 않는지 확인
- `NaN`, `Infinity`, 누락 열, 중복 Calibration 특성을 거부하는지 확인
- 특성 순서를 고정하고 텐서의 행·열 차원을 올바르게 유지하는지 확인
- 통계는 유효한 보정 데이터만 이용해 계산하는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 입력 형식 확인</strong></summary>

두 CSV의 필수 열과 자료형을 확인합니다. 숫자 변환 전에 원본 문자열을 보존하면 오류 행을 기록하기 쉽습니다.

```python
# TODO: 각 파일의 필수 열 검사
# TODO: 행별 누락값·숫자·범위 검증
```

</details>

<details>
<summary><strong>STEP 2. 정상·오류 기록 분리</strong></summary>

유효성 검사에서 통과한 행과 거부한 행을 분리합니다. 거부된 행의 ID 때문에 이후의 정상 기록이 중복으로 처리되지 않도록 검사 순서를 설계합니다.

```python
# TODO: 유효한 record_id만 중복 검사에 등록
# TODO: source_line과 error_code 기록
```

</details>

<details>
<summary><strong>STEP 3. 텐서 변환과 보정</strong></summary>

특성 순서를 고정한 후 값과 채널별 보정 계수를 텐서로 구성합니다. 보정 연산과 채널별 평균 계산은 직접 구현합니다.

```python
features = ["temperature", "humidity", "power_kw"]
values = torch.tensor(valid_df[features].to_numpy(dtype="float32"))

# TODO: 보정 파일을 Feature 순서에 맞춰 정렬
# TODO: Offset·Scale Tensor 구성 및 Broadcasting
# TODO: 채널별 평균 계산
```

</details>

<details>
<summary><strong>STEP 4. 출력 및 일관성 확인</strong></summary>

정상 행의 원래 순서, 결과 CSV의 행 수, 오류 코드별 건수, 보고서의 집계값을 확인합니다. 정상 샘플이 부족한 경우의 종료 규칙도 함께 적용합니다.

</details>

---

### A-02. 혼잡 예측 모델의 학습과 평가

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Dataset · DataLoader · [Chapter 06](../Chapter-06/README.md) · MLP · `BCEWithLogitsLoss` · [Chapter 07](../Chapter-07/README.md) · Training Loop

#### 문제 설명

시설의 혼잡 여부를 두 가지 이용 지표로 예측하려고 합니다. 데이터에는 직선 하나로 구분하기 어려운 패턴이 포함되어 있습니다. 학습·검증·테스트 데이터를 구분한 뒤, 학습한 모델을 간단한 Baseline과 비교해야 합니다.

PyTorch로 간단한 MLP를 학습한 뒤, 지정된 테스트 데이터에 대한 예측 결과를 기록하는 프로그램을 작성하십시오.

#### 요구사항

1. `usage.csv`의 `split` 값(`train`, `validation`, `test`)을 그대로 사용한다. 행을 다시 임의로 분할하지 않는다.
2. Model(모델) 입력 Feature(특성)는 `x1`, `x2` 두 개이며, Target `crowded`는 `0` 또는 `1`이다. 각 분할에는 두 클래스가 모두 존재한다고 가정한다.
3. Training(학습) 데이터만 사용해 특성별 평균과 표준편차를 계산하고, 세 분할에 같은 기준을 적용한다. 표준편차는 모집단 기준(`ddof=0`)으로 계산한다. 표준편차가 0인 특성은 Scale을 1로 처리한다.
4. `nn.Linear(2,12) → nn.ReLU() → nn.Linear(12,1)` 구조를 구현한다.
5. `BCEWithLogitsLoss`, `AdamW(lr=0.01)`, Batch Size 16, 최대 100 Epoch, `torch.manual_seed(42)`를 사용한다. Epoch마다 DataLoader를 사용하고 마지막 Batch를 버리지 않는다.
6. 매 Epoch의 학습 평균 Loss와 검증 Accuracy를 기록한다. **최종 선택 기준은 검증 Accuracy 최대, 동점이면 더 이른 Epoch**로 정한다.
7. 학습 데이터에서 가장 빈번한 클래스를 항상 예측하는 Majority Baseline도 계산한다. 빈도가 같다면 `0`을 선택한다.
8. 테스트 결과에 대한 Accuracy·F1·Confusion Matrix를 계산하고, `test_predictions.csv`를 생성한다. 예측 Label은 `torch.sigmoid(logit) ≥ 0.5`로 결정한다. 테스트 결과를 보고 모델을 다시 선택하지 않는다.

#### 입력 파일 규격

**`usage.csv`**

```csv
record_id,split,x1,x2,crowded
U001,train,-1.2,0.8,1
U002,train,0.4,0.5,0
U003,validation,1.1,-0.9,1
U004,test,-0.2,-0.3,0
```

실습 파일에는 학습·검증·테스트 분할마다 30개 이상의 샘플이 포함되어 있습니다. 각 데이터 행에는 서로 다른 `record_id`가 부여됩니다. `x1`, `x2`는 실수형으로 처리하며, 결측값이나 `NaN`, `Infinity`는 포함되지 않습니다.

#### 출력 파일 규격

- `training_history.csv`: `epoch,train_loss,validation_accuracy`
- `model_selection.json`: `best_epoch,best_validation_accuracy,train_majority_class,test_baseline_accuracy`
- `test_predictions.csv`: `record_id,actual,probability,predicted` (테스트 데이터의 원본 순서 유지, 확률은 소수점 넷째 자리까지 기록)
- `test_metrics.json`: `accuracy,f1,tp,fp,fn,tn` (반올림 전 확률로 예측 Label을 결정한 뒤 지표를 계산하며, F1의 분모가 0이면 0으로 기록)

<!-- 예시 결과 이미지 추가 예정 (정답 코드 실행 후 생성)
삽입 파일: ./assets/problems/a-02-training-history.png
내용: 학습 Loss와 검증 Accuracy의 Epoch별 변화를 함께 확인하는 그래프. 실제 정답 코드 실행에서 생성하며 최적 Epoch를 표시할 것.
주의: 이미지를 평가용 필수 출력물로 간주하지 않음. 검증되지 않은 수치나 예시 결과를 임의로 만들지 말 것.
-->

#### 검증 기준

- Train만으로 계산한 Scaling 기준을 검증·테스트에 적용하는지 확인
- Loss에 Sigmoid가 중복 적용되지 않는지 확인
- 마지막 Batch의 크기에 맞춰 학습 Loss를 집계하는지 확인
- 모델 선택은 검증으로 수행하고 테스트는 한 번만 평가하는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 데이터 구성</strong></summary>

`split`에 지정된 분할을 유지하고, 학습 데이터만으로 전처리 기준을 계산합니다. 입력 텐서는 `(N, 2)`, 정답 텐서는 `(N, 1)` 형태로 구성합니다.

```python
# TODO: 데이터 분할 및 전처리 기준 계산
# TODO: TensorDataset과 DataLoader 구성
```

</details>

<details>
<summary><strong>STEP 2. 학습 반복</strong></summary>

각 Batch에서 Forward, Loss 계산, Gradient 계산, Optimizer를 이용한 파라미터 갱신을 순서대로 수행합니다. 평균 Loss를 구할 때는 각 Batch에 포함된 샘플 수를 반영합니다.

```python
for x_batch, y_batch in train_loader:
    optimizer.zero_grad(set_to_none=True)
    logits = model(x_batch)
    # TODO: Loss 계산
    # TODO: Gradient 계산
    # TODO: 파라미터 갱신
```

</details>

<details>
<summary><strong>STEP 3. 검증과 가중치 보관</strong></summary>

매 Epoch마다 검증 Accuracy를 계산하고, 정해진 동점 처리 기준에 따라 가장 좋은 Weight를 선택합니다. 선택한 Weight는 이후 학습 과정에서 변경되지 않도록 별도의 사본으로 보관합니다.

```python
# TODO: 검증 Accuracy 계산
# TODO: Best Epoch와 Weight 보존
```

</details>

<details>
<summary><strong>STEP 4. 독립 평가</strong></summary>

보관한 Weight를 복원한 뒤 테스트 데이터에서 최종 성능을 평가합니다. 테스트 결과를 기준으로 모델을 다시 선택하거나 전처리 기준을 변경하지 않습니다.

</details>

---

### A-03. 학습 설정 비교 실험

**관련 개념:** [Chapter 07](../Chapter-07/README.md) · SGD · AdamW · Learning Rate · Fair Comparison · Reproducibility

#### 문제 설명

데이터센터의 전력 사용량을 예측하기 위해 MLP를 학습합니다. 서로 다른 Optimizer 설정에 따른 성능 차이를 비교하되, 초기 Weight나 데이터 순서가 달라지지 않도록 조건을 통제해야 합니다.

**초기 Parameter(파라미터), 데이터 분할, Epoch 수, Batch 순서**를 동일하게 유지하며 두 학습 설정을 비교하는 실험 프로그램을 작성하십시오.

#### 요구사항

1. `energy.csv`에 명시된 `train`, `validation`, `test` 분할을 유지한다. Training(학습) 데이터에서만 Feature(특성) Scaling 기준을 계산한다. 표준편차는 모집단 기준(`ddof=0`)을 사용하고, 0이면 1로 대체한다.
2. 입력 특성은 `occupancy`, `temperature_c`, `weekend`이고 Target은 `energy_kwh`이다. 회귀 MLP는 `Linear(3,16) → ReLU → Linear(16,1)`이다.
3. 같은 Seed 42로 생성한 초기 `state_dict`를 두 후보에 각각 복사한다. Epoch별 Shuffle 순서도 두 후보에 동일하게 적용한다.
4. 후보 A는 `SGD(lr=0.02, momentum=0.9)`, 후보 B는 `AdamW(lr=0.01, weight_decay=0.01)`이다. 이 비교는 **Optimizer와 학습률을 포함한 두 설정의 비교** 이지, Optimizer 종류만 바꾸는 통제 실험은 아니다.
5. Batch Size 16, 최대 30 Epoch, MSELoss로 학습한다. Epoch 평균 Loss는 Sample(샘플) 수를 반영한다.
6. 매 Epoch의 Validation(검증) RMSE를 기록하고, 각 후보의 최저 검증 RMSE에 해당하는 Weight를 별도로 보관한다.
7. 후보별 최저 검증 RMSE를 비교하여 가장 낮은 값을 기록한 설정을 선택한다. 동점이면 후보 A를 선택한다. 선정된 설정의 Best Weight로 테스트 데이터를 한 번만 평가한다.

#### 입력 파일 규격

**`energy.csv`**

```csv
record_id,split,occupancy,temperature_c,weekend,energy_kwh
E001,train,35,20,0,96
E002,train,61,23,0,129
E003,validation,47,22,1,114
E004,test,53,19,0,120
```

- 각 데이터 행에는 서로 다른 `record_id`가 부여됩니다.
- `weekend`는 `0` 또는 `1`이며, `occupancy`와 `energy_kwh`는 `0` 이상의 유한한 실수입니다.
- 학습·검증·테스트 데이터에는 각각 30개 이상의 샘플이 포함됩니다.

#### 출력 파일 규격

- `training_history.csv`: `candidate,epoch,train_loss,validation_rmse`
- `comparison.json`: 각 후보의 `optimizer`, `learning_rate`, `best_epoch`, `best_validation_rmse` 및 최종 선정된 후보를 나타내는 `selected_candidate`
- `test_predictions.csv`: `record_id,actual,predicted`
- `test_metrics.json`: 선정된 모델의 `mae,rmse`

모델 선택은 검증 RMSE를 기준으로 수행하며, 테스트 데이터는 최종 성능 평가에만 사용합니다. 또한 모델 비교 결과를 해석할 때는 Optimizer 종류뿐 아니라 학습률 등 다른 설정도 함께 고려해야 합니다.

#### 검증 기준

- 첫 Epoch 전에 두 후보의 파라미터가 실제로 동일한지 확인
- 동일한 샘플 순서를 사용했는지, Optimizer 상태가 후보 간 공유되지 않는지 확인
- 학습 Loss와 검증 RMSE를 구분하여 계산했는지 확인
- Best Epoch가 마지막 Epoch가 아닐 때도 해당 Weight로 테스트를 수행하는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 실험 공통 조건 준비</strong></summary>

두 후보가 동일한 초기 Weight와 전처리 기준을 사용하도록 준비합니다. 초기 모델의 `state_dict`는 학습 과정에서 변경되지 않도록 별도의 복사본으로 보관합니다.

```python
torch.manual_seed(42)
initial_model = make_model()
# TODO: 초기 state_dict를 독립적인 복사본으로 보관
```

</details>

<details>
<summary><strong>STEP 2. 후보별 학습</strong></summary>

각 후보에 사용할 모델과 Optimizer를 별도로 생성합니다. Epoch마다 두 후보가 동일한 순서로 샘플을 학습하도록 Shuffle 조건을 맞춥니다.

```python
# TODO: 후보별 초기 상태 복원
# TODO: 동일한 배치 순서로 학습
```

</details>

<details>
<summary><strong>STEP 3. 검증 결과 비교</strong></summary>

Epoch마다 검증 RMSE를 계산하고, 각 후보에서 가장 낮은 RMSE를 기록한 시점의 Weight를 보관합니다. 결과를 비교할 때는 Optimizer 종류뿐 아니라 학습률 등의 설정 차이도 고려합니다.

</details>

<details>
<summary><strong>STEP 4. 최종 모델 평가</strong></summary>

검증 RMSE를 기준으로 선정한 후보의 최적 Weight를 복원하고, 테스트 데이터에서 최종 성능을 평가합니다. 결과 파일에 평가 지표가 올바르게 기록되었는지, 예측 결과가 원본 데이터 순서대로 저장되었는지 확인합니다.

</details>

---

### A-04. 모델 인계와 추론 결과 검증

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Dtype · Device · [Chapter 06](../Chapter-06/README.md) · `state_dict` · Inference · [Chapter 07](../Chapter-07/README.md) · Reproducibility

#### 문제 설명

실험 환경에서 학습한 모델을 다른 담당자가 추론에 사용하려고 합니다. Weight 파일만 전달해서는 학습 당시의 Feature(특성) 순서나 Scaling 기준을 정확히 재현하기 어려우며, 예측 결과도 달라질 수 있습니다.

학습과 추론을 **서로 다른 프로세스로 실행** 하고, 저장·복원 후에도 같은 입력에 대해 일관된 예측을 얻도록 프로그램을 작성하십시오.

#### 요구사항

1. `training.csv`의 `split`을 유지한다. 특성은 `temperature_c`, `vibration`, `hours_active` 세 개이고 Binary Target은 `needs_service`이다.
2. 학습 데이터에서만 평균·표준편차를 구한다. 표준편차는 모집단 기준(`ddof=0`)으로 계산하고, 0이면 1로 대체한다.
3. `Linear(3,8) → ReLU → Linear(8,1)` 모델을 만들고 `BCEWithLogitsLoss`, `AdamW(lr=0.01)`로 최대 50 Epoch 학습한다. Best Validation(검증) Loss를 기준으로 Weight를 선택한다.
4. 모델의 `state_dict`를 `model_weights.pt`에 저장하고 특성 순서·Scaling 기준·Target·예측 Threshold 0.5를 `preprocessing.json`에 기록한다.
5. 별도 `predict` 실행에서는 학습 CSV를 읽지 않고 저장 파일과 `incoming.csv`만 사용한다. CSV 열의 순서가 달라져도 **이름을 기준으로** 동일한 특성 순서를 복원한다.
6. 신규 데이터에서 특성값이 누락되거나 숫자가 유효하지 않은 행, `record_id`가 중복된 행은 거부하고 사유를 기록한다. 필수 열 자체가 누락되었으면 추론을 중단한다.
7. 원래 모델과 새 프로세스에서 복원한 모델의 동일한 테스트 입력에 대한 확률 차이는 CPU 환경에서 `1e-6` 이하여야 한다.

#### 입력 파일 규격

**`training.csv`**

```csv
record_id,split,temperature_c,vibration,hours_active,needs_service
T01,train,30,2.1,180,0
T02,train,42,5.8,260,1
T03,validation,37,4.0,230,1
T04,test,32,2.5,210,0
```

**`incoming.csv`** (특성 순서를 바꾼 예시)

```csv
record_id,hours_active,temperature_c,vibration
N01,220,34,3.1
N02,280,44,6.2
```

#### 출력 파일 규격

- `model_weights.pt`: 검증 Loss를 기준으로 선택한 모델의 Weight
- `preprocessing.json`: 특성 순서, Scaling 기준, Target, 예측 Threshold
- `test_predictions.csv`: `record_id,actual,probability,predicted`
- `incoming_predictions.csv`: `record_id,probability,predicted`
- `rejected_rows.csv`: `record_id,error_code` (오류 코드는 `INVALID_VALUE`, `DUPLICATE_ID`)
- `handoff_report.json`: `feature_order`, `test_accuracy`, `reload_max_abs_diff`

예측 확률은 소수점 여섯째 자리까지 기록합니다. 원본 모델과 복원한 모델의 예측 결과를 비교할 때는 **반올림 전** 확률을 사용합니다.
`torch.load()`는 프로젝트에서 생성한 신뢰할 수 있는 파일에 한해 사용하며, `weights_only=True` 옵션을 적용합니다.

#### 검증 기준

- `incoming.csv`의 특성 열 순서가 달라도 동일한 예측 결과가 나오는지 확인
- 추론 과정에서 `eval()`과 `torch.no_grad()`를 올바르게 적용했는지 확인
- 잘못된 Dtype·Shape, 필수 특성 누락, Scaling 기준 불일치를 감지하는지 확인
- 마지막 Epoch가 아닌 최저 검증 Loss를 기준으로 선택한 Weight가 저장·복원되는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 학습 결과 정리</strong></summary>

모델의 Weight뿐 아니라 입력 특성의 순서, Scaling 기준, 모델 구조, 자료형, 예측 Threshold도 함께 보관합니다. 별도의 프로세스에서도 동일한 모델과 전처리 과정을 재현할 수 있도록 저장 방식을 설계합니다.

```python
feature_order = ["temperature_c", "vibration", "hours_active"]
# TODO: 학습 결과 및 전처리 정보 저장
```

</details>

<details>
<summary><strong>STEP 2. 독립 추론 실행</strong></summary>

학습에 사용한 메모리 객체에 의존하지 않고, 저장된 파일을 불러와 별도의 프로세스에서 모델을 복원합니다. 필요한 파일이 없거나 저장된 정보가 모델 구조와 일치하지 않으면 추론을 중단합니다.

</details>

<details>
<summary><strong>STEP 3. 입력 특성 정렬</strong></summary>

CSV의 열 위치와 관계없이 특성 이름을 기준으로 입력 순서를 맞춥니다. 저장된 Scaling 기준을 적용한 뒤 복원한 모델로 예측을 수행합니다.

```python
# TODO: 저장된 정보에 따라 입력 열 정렬
# TODO: 저장된 기준으로 Scaling
# TODO: 모델 복원 및 추론
```

</details>

<details>
<summary><strong>STEP 4. 정합성 검증</strong></summary>

학습 당시의 모델과 새 프로세스에서 복원한 모델에 동일한 입력을 적용합니다. 두 모델의 예측 확률을 반올림 전 값으로 비교하고, 최대 절댓값 차이가 허용 범위 이내인지 확인합니다.

</details>

---
## Professional

### P-01. 설비 고장 위험 예측과 정비 우선순위 결정

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · DataLoader · [Chapter 06](../Chapter-06/README.md) · Binary MLP · [Chapter 07](../Chapter-07/README.md) · `pos_weight` · Early Stopping · Group Split · Threshold

#### 문제 설명

여러 사업장에서 설비의 온도, 진동, 경보 횟수를 수집합니다. 정비팀은 앞으로 7일 안에 고장이 발생할 가능성이 높은 설비를 파악하려고 합니다. 고장 사례는 드물고, 같은 사업장의 장비들은 사용 환경을 공유합니다. 따라서 데이터를 무작위로 분할하면 새로운 사업장에서의 모델 성능을 과대평가할 수 있습니다.

**PyTorch 학습 파이프라인**을 구축하고, 클래스 불균형에 대응하는 Loss와 Early Stopping을 적용하십시오. 사업장 단위로 성능을 평가한 뒤, 제한된 정비 인력을 고려한 경보 정책까지 구현해야 합니다.

#### 제공 데이터

모든 CSV는 UTF-8 형식의 실습용 합성 데이터입니다. 과거 기록에는 최소 12개 사업장과 400개 이상의 유효 Sample(샘플)이 포함됩니다.

**`maintenance_history.csv`**

| 열 이름 | 의미 | 사용 기준 |
|---|---|---|
| `record_id` | 관측 기록 ID | 중복 확인·결과 추적 |
| `site_id` | 사업장 ID | 그룹 분할 기준 |
| `asset_id` | 설비 ID | 운영 예측 정렬·추적 |
| `recorded_date` | 관측 날짜 | 날짜별 운영 정책에 사용 |
| `temperature_c` | 온도 | Feature(특성) |
| `vibration_mm_s` | 진동 | 특성 |
| `alarm_count_7d` | 최근 7일 경보 건수 | 특성 |
| `operating_hours` | 누적 작동 시간 | 특성 |
| `failure_next_7d` | 관측 뒤 7일 이내 고장 여부(0·1) | Target 전용 |
| `final_repair_cost` | 고장 이후 확정 수리비 | **특성 사용 금지** |

**`incoming_maintenance.csv`** 는 `failure_next_7d`, `final_repair_cost`가 없는 신규 관측 기록입니다. 신규 입력에는 과거 학습 데이터에 없던 `site_id`가 포함될 수 있습니다. `site_id`와 `asset_id`는 모델 입력 특성으로 사용하지 않습니다.

#### 요구사항

1. **입력 검증:** 필수 열 누락, `record_id` 중복, 날짜 오류, 결측값, 비유한 수치를 확인한다. 네 숫자 특성 가운데 `vibration_mm_s`, `alarm_count_7d`, `operating_hours`는 음수일 수 없으며 경보 건수는 정수여야 한다. 무효 행은 `invalid_records.csv`로 분리한다.
2. **그룹 분할:** 고유 `site_id`를 기준으로 학습 약 60%, 검증 약 20%, 테스트 약 20%로 나눈다. `GroupShuffleSplit(random_state=42)`을 이용할 수 있다. 사업장 ID의 교집합은 모두 비어 있어야 한다. 그룹별 행 수가 달라 전체 샘플 비율은 다를 수 있다.
3. **Scaling:** 허용된 네 숫자 특성만 사용한다. 평균·표준편차는 Training(학습)에서 계산하고 검증·테스트·Incoming에 그대로 적용한다. `final_repair_cost`와 Target을 특성에 혼합하지 않는다.
4. **Baseline:** 학습 다수 클래스를 예측하는 모델을 기준으로 두고 테스트 Accuracy·Recall·F2를 함께 기록한다.
5. **신경망:** `Linear(4,16) → ReLU → Linear(16,8) → ReLU → Linear(8,1)`을 구성한다. `BCEWithLogitsLoss(pos_weight=...)`의 가중치는 **학습 데이터의 음성 수를 양성 수로 나눈 값**으로 계산한다. 학습에 양성 또는 음성이 하나도 없으면 학습을 중단하고 이유를 기록한다.
6. **학습:** `AdamW(lr=0.003, weight_decay=0.01)`, Batch Size 32, 최대 80 Epoch를 사용한다. 검증 Loss 기준 Patience 8로 Early Stopping을 수행하고 Best Weight를 복원한다. 동일한 Seed 42와 CPU 실행을 기본 검증 환경으로 설정한다.
7. **Threshold 선택:** 검증에서 `[0.25,0.40,0.55,0.70]` 중 F2가 최대인 Threshold를 선택한다. 동점이라면 더 큰 Threshold를 선택한다. 테스트에서 Threshold를 재선택하지 않는다.
8. **운영 정책:** Incoming에 선택된 Threshold를 적용한다. Threshold를 통과한 설비 중 **사업장·날짜별 최대 5대의 고유 설비**를 선정한다. 동일 설비에 여러 기록이 있다면 확률이 가장 높은 기록을 대표로 택하고, 확률이 같으면 `record_id` 오름차순으로 정한다. 대표 기록끼리는 점수 내림차순, 동점이면 `asset_id`, 다시 동점이면 `record_id` 오름차순으로 정렬한다. 나머지 기록에는 미선정 사유를 남긴다.
9. **인계:** 특성 순서·Scaling 기준·Threshold·Best Epoch·Weight를 저장하고, 재로딩 후 동일 샘플의 예측 결과가 일치하는지 확인한다.

#### 입력 예시

```csv
record_id,site_id,asset_id,recorded_date,temperature_c,vibration_mm_s,alarm_count_7d,operating_hours,failure_next_7d,final_repair_cost
M001,S01,A01,2026-03-01,38,4.1,2,820,0,0
M002,S02,A14,2026-03-01,51,8.2,7,1130,1,230000
```

위 표는 Schema 예시이며, 실제 학습용 파일에는 여러 사업장과 충분한 양성·음성 샘플이 포함됩니다.

#### 출력 파일 규격

- `invalid_records.csv`: `source_file,source_line,record_id,error_code`
- `split_audit.json`: 분할별 샘플·Site 수와 Site ID 교집합 크기
- `training_history.csv`: `epoch,train_loss,validation_loss`
- `evaluation.json`: `best_epoch`, `pos_weight`, `threshold`, Baseline 및 모델의 테스트 Accuracy·Recall·F2·Confusion Matrix
- `incoming_priorities.csv`: `record_id,site_id,asset_id,recorded_date,probability,selected,status` (`SELECTED`, `BELOW_THRESHOLD`, `CAPACITY_LIMIT`, `DUPLICATE_ASSET`)
- `model_weights.pt`, `preprocessing.json`

평가 점수에 일률적인 하한을 두지는 않습니다. 데이터 분할의 독립성과 운영 정책을 정확히 구현했는지를 함께 확인합니다.

#### 검증 기준

- 중복 Site 없이 분할되었는지, 학습 이후에만 얻을 수 있는 정보를 특성에서 제외했는지 확인
- `pos_weight`와 Scaling에 테스트 또는 Incoming 정보가 섞이지 않았는지 확인
- Best 검증 Loss가 발생한 Epoch의 Weight를 선택했는지 확인
- 테스트 성능과 Incoming 우선 검토 목록을 별도 결과로 보관했는지 확인
- 사업장·날짜별 선정 한도와 동점 규칙, 유효하지 않은 운영 기록의 처리 결과를 확인

#### HELP

<details>
<summary><strong>STEP 1. 데이터·평가 체계 설계</strong></summary>

사업장 단위 분할과 입력 검증을 먼저 설계합니다. 그룹별 클래스 분포를 확인하고, Target이나 사후 확정 정보가 학습에 포함되지 않는지 점검합니다.

</details>

<details>
<summary><strong>STEP 2. 학습·모델 선택 정책 설계</strong></summary>

클래스 불균형을 반영한 Loss, Early Stopping, 검증 데이터에서의 Threshold 선택을 연결합니다. 선택 기준과 모델 상태를 재현 가능하게 보관합니다.

```python
# TODO: 학습 분할의 클래스 분포에 따른 Loss 구성
# TODO: 최적 Weight와 Threshold 선택 정책
```

</details>

<details>
<summary><strong>STEP 3. 운영 우선순위와 인계 검증</strong></summary>

평가용 예측과 실제 정비 대상 선정은 별도로 수행합니다. 사업장·날짜별 중복 설비 처리, 선정 한도, 미선정 사유와 재로딩 후 일치성을 검증합니다.

</details>

---

### P-02. 시간 흐름을 반영한 전력 수요 예측

**관련 개념:** [Chapter 06](../Chapter-06/README.md) · Regression MLP · [Chapter 07](../Chapter-07/README.md) · Temporal Split · Scheduler · Early Stopping · Residual Analysis

#### 문제 설명

소형 전력망 운영자는 각 지역의 다음 날 전력 수요를 예측해 공급 계획을 조정합니다. 예측 시점 이후에 확정된 수요를 Feature(특성)로 사용하거나 과거와 미래의 기록을 무작위로 섞으면, 평가 결과가 실제 운영 성능을 제대로 반영하지 못할 수 있습니다.

미래 정보가 섞이지 않도록 데이터를 날짜별로 분할하십시오. 이어서 전력 수요 예측 MLP의 학습, Learning Rate Scheduler 적용, 예측 오차 분석과 모델 저장 기능을 구현하십시오.

#### 제공 데이터

**`microgrid_daily.csv`** 에는 다음 열이 포함됩니다.

```csv
grid_id,date,energy_kwh,temperature_c,weekday,holiday,alarm_count,next_day_energy_kwh
G01,2026-01-01,120,8,3,1,0,127
G02,2026-01-01,96,8,3,1,1,92
G01,2026-01-02,127,7,4,0,0,122
```

- 관측 종료 시점에 이용 가능한 특성: `energy_kwh`, `temperature_c`, `weekday`, `holiday`, `alarm_count`
- Target: `next_day_energy_kwh` (다음 날 확정되는 값)
- `weekday`는 `0`(월요일)부터 `6`(일요일)까지, `holiday`는 0 또는 1
- 같은 `grid_id`와 `date`의 조합이 반복되어서는 안 됩니다. 실제 파일에는 날짜마다 5개 이상 구역의 기록이 포함됩니다.

#### 요구사항

1. **무결성 검사:** 날짜가 올바른 ISO 형식인지, `(grid_id,date)`가 중복되지 않는지, 필수 수치가 유한한지 확인한다. `energy_kwh`, `alarm_count`, `next_day_energy_kwh`는 음수일 수 없다. 유효하지 않은 행은 오류 사유를 포함해 별도로 기록한다.
2. **Temporal Split:** 정상 기록의 고유 날짜를 오름차순으로 정렬한다. 첫 60% 날짜는 학습, 다음 20%는 검증, 마지막 20%는 테스트로 나누되 **각 구간 사이의 경계 날짜 1일씩을 Gap으로 제외** 한다. 이 문서에서는 `floor(0.6D)`, `floor(0.2D)`를 기준으로 날짜 구간을 먼저 나눈 뒤 학습과 검증 구간의 마지막 날짜를 제외하는 방법으로 통일한다. `D`는 고유 날짜 수이며, 최소 40일의 **연속된 달력 날짜**가 제공된다. 따라서 경계에서 제외하는 각 날짜는 달력 기준 1일에 해당한다.
3. **Baseline:** 관측 당일 `energy_kwh`를 다음 날 수요의 예측값으로 사용하는 Persistence Baseline을 구현한다.
4. **신경망:** 위 5개 특성을 입력받는 `Linear(5,24) → ReLU → Linear(24,1)`을 학습한다. 특성 Scaling은 학습 데이터에서만 계산한다. `MSELoss`, `AdamW(lr=0.003)`, Batch Size 32를 사용한다.
5. **학습 제어:** 최대 120 Epoch 동안 검증 RMSE를 계산하고, `ReduceLROnPlateau(mode="min", factor=0.5, patience=5)`로 학습률을 조정한다. Early Stopping은 검증 RMSE 기준 Patience 15를 사용하고 Best Weight를 복원한다.
6. **결과 평가:** 최종 테스트에서 Baseline과 MLP의 MAE·RMSE를 계산한다. 구역별 MAE와 `actual - predicted`인 Residual을 함께 기록하고, 가장 큰 과소 예측 5건을 기록한다. 과소 예측은 `actual - predicted`가 큰 순서이며 동점은 `date`, `grid_id` 오름차순으로 정한다.
7. **모델 전달:** Best Weight, Scaling 기준, 학습 설정, 데이터 분할 날짜를 저장하고, 재로딩된 모델의 추론 결과를 비교한다.

#### 출력 파일 규격

- `invalid_daily.csv`: `source_line,grid_id,date,error_code`
- `split_dates.json`: Train·검증·테스트 날짜 수와 경계·Gap 날짜
- `training_history.csv`: `epoch,train_mse,validation_rmse,learning_rate`
- `model_comparison.json`: 테스트 Baseline 및 MLP의 `mae,rmse`, `best_epoch`
- `test_predictions.csv`: `grid_id,date,actual,baseline_prediction,model_prediction,residual`
- `grid_report.csv`: `grid_id,sample_count,mae`
- `underprediction_top5.csv`: `grid_id,date,actual,model_prediction,residual`
- `model_weights.pt`, `preprocessing.json`

예측값과 오차는 CSV에 소수점 넷째 자리까지 기록합니다. 평가 지표는 반올림 전 값으로 계산합니다.

<!-- 예시 결과 이미지 추가 예정 (정답 코드 실행 후 생성)
삽입 파일: ./assets/problems/p-02-demand-forecast.png
내용: 실제 테스트 구간의 정답 수요·Baseline·모델 예측을 날짜별로 비교한 그래프. 실제 실행 결과 사용, 구역 선택과 단위 명시.
주의: 이미지를 평가용 필수 출력물로 간주하지 않음. 검증되지 않은 수치나 예시 결과를 임의로 만들지 말 것.
-->

#### 검증 기준

- 동일한 날짜의 Sample(샘플)이 서로 다른 분할에 섞이지 않는지 확인
- Train과 검증 사이, 검증과 테스트 사이에서 Target의 다음 날 정보가 넘어가지 않도록 Gap을 적용했는지 확인
- `scheduler.step(validation_rmse)`가 검증 측정 후 실행되는지 확인
- Best Model(모델)의 테스트 점수만 최종 기록하고, 테스트 지표로 Early Stopping을 조정하지 않는지 확인
- 전력 사용량이 0인 날짜와 과소 예측이 큰 날짜를 올바르게 처리하는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 날짜 기준과 데이터 흐름 설계</strong></summary>

관측일과 다음 날 Target의 관계를 먼저 정리합니다. 날짜 경계와 Gap을 분할 전에 확정하고, Scaling 기준에는 학습 구간만 사용합니다.

</details>

<details>
<summary><strong>STEP 2. 학습 제어와 모델 선택</strong></summary>

학습률 변경과 Early Stopping의 기준 지표를 일관되게 관리합니다. Epoch별 검증 결과와 선택된 Weight를 보관할 구조를 직접 설계합니다.

```python
# TODO: 검증 RMSE를 기준으로 Scheduler 실행
# TODO: Best Weight·Patience 관리
```

</details>

<details>
<summary><strong>STEP 3. 운영 관점의 오류 분석</strong></summary>

Baseline과 모델을 같은 테스트 구간에서 평가합니다. 전체 오차뿐 아니라 구역별 편차와 큰 과소 예측 사례를 함께 분석합니다.

</details>

---

### P-03. 제한된 자원에서의 모델 학습 설계

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · DataLoader · [Chapter 06](../Chapter-06/README.md) · Parameter Count · [Chapter 07](../Chapter-07/README.md) · Effective Batch · Gradient Accumulation · Clipping · Fair Comparison

#### 문제 설명

제한된 CPU 환경에서 모델을 학습하는 팀은 모델 크기와 학습 예산을 신중하게 정해야 합니다. 모델이 크다고 반드시 좋은 결과를 얻는 것은 아닙니다. 같은 학습 예산에서 실행 시간을 측정하고, Batch Size가 제한된 상황에서도 Gradient를 정확히 계산해 성능과 자원 사용량을 함께 비교해야 합니다.

두 모델 구조와 두 Batch 처리 전략을 비교하여 제한된 자원에 적합한 구성을 선택하십시오.

#### 제공 데이터

`quality_train.csv`는 다음 형식의 Binary Classification 데이터입니다. 모든 행은 합성 데이터이며, `split`은 `train`, `validation`, `test` 중 하나입니다.

```csv
record_id,split,f1,f2,f3,f4,defective
Q001,train,0.3,12,2.1,5,0
Q002,train,0.8,20,4.3,3,1
Q003,validation,0.5,18,3.1,4,1
Q004,test,0.1,9,1.5,6,0
```

실제 파일에는 각 분할마다 최소 50개 Sample(샘플)이 포함됩니다. Feature(특성)는 유한한 수치이며, Target은 0 또는 1입니다.

#### 요구사항

1. **모델 후보:** 구조 S는 `Linear(4,8) → ReLU → Linear(8,1)`, 구조 L은 `Linear(4,32) → ReLU → Linear(32,16) → ReLU → Linear(16,1)`이다. 각각의 학습 가능한 Parameter(파라미터) 수를 기록한다.
2. **실험 조건:** `torch.manual_seed(42)`, CPU, `num_workers=0`을 기준으로 한다. `BCEWithLogitsLoss`와 `AdamW(lr=0.005)`를 사용한다. Train의 전처리 기준과 분할은 모든 후보가 공유한다.
3. **업데이트 예산:** 각 후보가 최대 **120회 Optimizer Update**까지만 수행하도록 한다. Epoch 수는 데이터셋 크기에 따라 달라질 수 있으며 Update 횟수로 예산을 비교한다. 같은 후보를 비교할 때는 동일한 초기 Weight와 샘플 순서를 사용한다.
4. **Effective Batch Size 64:** 방법 A는 가능한 경우 한 번에 최대 64개 샘플을 처리한다. 방법 B는 최대 32개 샘플로 구성된 Micro-Batch를 순차적으로 처리하며, **64개 샘플에 해당하는 Gradient를 누적한 뒤 Optimizer Update를 한 번 수행**한다. 마지막 Batch에 남은 샘플이 64개보다 적어도 버리지 않는다. 이때는 실제 샘플 수를 기준으로 평균 Loss를 계산한다.
5. **Gradient Clipping:** 각 Optimizer Update 직전, 누적된 Gradient에 `clip_grad_norm_(..., max_norm=1.0)`을 한 번 적용한다. Micro-Batch마다 개별 Clipping을 수행하지 않는다.
6. **비교 결과:** 각 구성에서 Validation(검증) Accuracy와 Loss, Update 수, 파라미터 수, 실제 학습 시간을 기록한다. 단일 실행 시간만으로 판단하지 않도록 **각 설정 3회 측정값의 중앙값**을 기록한다. 시간은 전처리·검증·파일 저장을 제외한 학습 Update 구간에서 측정한다. 측정용 실행에서는 매번 초기 상태를 복원한다.
7. **모델 선택:** 세 번 실행한 검증 Accuracy의 평균이 가장 높은 설정을 선택하고, 동점이면 중앙 실행 시간이 더 짧은 구성을 선택한다. 중앙값까지 동일하면 구조 S, 그다음 방법 A를 우선한다. 확정 후 테스트 Accuracy·F1을 한 번 계산한다.
8. **결과 해석:** Micro-Batch 결과가 실제 Batch 방식과 얼마나 다른지 비교한다. CPU 부동소수점 연산 순서에 따른 작은 차이는 허용하며, 모델 크기와 수행 시간만으로 정확도를 보장하지 않는다.

#### 출력 파일 규격

- `runs.csv`: `architecture,batch_strategy,run_id,optimizer_updates,validation_loss,validation_accuracy,elapsed_seconds`
- `comparison.csv`: `architecture,batch_strategy,parameter_count,median_seconds,mean_validation_accuracy`
- `selected_model.json`: `architecture,batch_strategy,best_validation_accuracy,test_accuracy,test_f1`
- `gradient_audit.json`: 동일한 초기 Weight·입력에서 실제 Batch와 Micro-Batch로 계산한 Gradient의 최대 절댓값 차이
- `training_report.md`: 실험 조건, 학습 예산, 마지막 Batch 처리 방식, 실제 차이의 해석

학습 시간은 CPU 환경에 따라 달라질 수 있습니다. 실행 시간이 **특정 초 이하**여야 한다는 조건은 없습니다. 다만 빠르게 실행되더라도 Gradient 계산이나 평가 결과가 잘못되었다면 완성으로 인정하지 않습니다.

<!-- 예시 결과 이미지 추가 예정 (정답 코드 실행 후 생성)
삽입 파일: ./assets/problems/p-03-resource-comparison.png
내용: 네 구성(S/A, S/B, L/A, L/B)의 검증 Accuracy와 실행 시간 중앙값을 비교한 그래프. 실제 3회 측정 결과만 사용.
주의: 이미지를 평가용 필수 출력물로 간주하지 않음. 검증되지 않은 수치나 예시 결과를 임의로 만들지 말 것.
-->

#### 검증 기준

- Update 수와 Epoch 수를 혼동하지 않았는지 확인
- Micro-Batch별 Loss를 실제 샘플 수에 따라 가중하여, 하나의 Effective Batch에 대한 평균 Gradient를 계산했는지 확인
- Dataset 크기가 64의 배수가 아니어도 마지막 샘플까지 학습에 사용하는지 확인
- 동일 후보의 반복 실험에서 초기 Weight와 난수 조건을 복원했는지 확인
- 검증의 설정 선택과 최종 테스트 평가를 분리했는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 학습 예산과 실험 설계</strong></summary>

실험별 초기 조건, 배치 순서, Update 예산과 시간 측정 구간을 정합니다. 비교 결과가 실행 순서의 차이로 달라지지 않는지 확인합니다.

</details>

<details>
<summary><strong>STEP 2. Batch 전략과 Gradient 관리</strong></summary>

실제 Batch와 Gradient Accumulation이 같은 샘플을 처리하도록 구성합니다. 마지막 Batch의 샘플 수가 64개보다 적은 경우에도 해당 샘플을 모두 사용하고, 실제 샘플 수를 반영하여 Loss를 계산합니다. Gradient Clipping은 각 Optimizer Update 직전에 한 번만 적용합니다.

```python
# TODO: Effective Batch의 실제 샘플 수를 반영한 Loss 누적
# TODO: 누적 후 Gradient Clipping 및 Optimizer Update
```

</details>

<details>
<summary><strong>STEP 3. 결과 비교와 선택 근거</strong></summary>

각 설정의 정확도, Loss, 파라미터 수, 실행 시간 중앙값을 함께 기록합니다. 계산 결과의 작은 수치 차이와 실질적 성능 차이를 구분해 기록합니다.

</details>

---
## Challenge

### C-01. 중단된 학습의 원인 분석과 복구

**관련 개념:** [Chapter 06](../Chapter-06/README.md) · `state_dict` · Dropout · [Chapter 07](../Chapter-07/README.md) · Optimizer State · Scheduler State · RNG · Resume

#### 문제 설명

설비 고장 예측 모델을 총 20 Epoch 동안 학습하던 중, 8번째 Epoch가 끝난 직후 전원이 차단되었습니다. 담당자는 Weight를 저장해 두었으므로 학습을 이어갈 수 있다고 생각했지만, 재개 후 결과는 중단 없이 학습했을 때와 달랐습니다.

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

제공된 코드와 실행 이력을 비교하여 결과가 달라진 원인을 파악하십시오. 복구 보고서에는 저장·복원해야 할 상태와 각 상태의 역할도 정리하십시오.

**목표는 높은 Accuracy를 얻는 것이 아니라, 중단 후 재개한 학습의 결과를 지정된 조건에서 연속 실행 결과와 일치시키는 것입니다.**

#### 제공 데이터와 실행 조건

- `train.csv`: `record_id,f1,f2,f3,f4,label` 형식의 실습용 합성 데이터
- `validation.csv`: 동일한 형식의 독립 검증 데이터
- Model(모델): `Linear(4,16) → ReLU → Dropout(0.2) → Linear(16,1)`
- Loss: `BCEWithLogitsLoss`, Optimizer: `AdamW(lr=0.005)`, Scheduler: `StepLR(step_size=5,gamma=0.5)`
- Batch Size 16, Epoch 20, CPU, `num_workers=0`
- 데이터 순서는 매 Epoch마다 Shuffle하며, 이를 위해 사용되는 `torch.Generator`의 상태까지 추적한다.
- 비교용 실행은 동일한 입력 파일과 라이브러리 버전, Thread 설정에서 수행한다.

#### 요구사항

1. **기준 실행:** 같은 초기 Weight와 Seed를 사용하여 20 Epoch를 중단 없이 학습하고, Epoch별 Training(학습) Loss·검증 Loss·Learning Rate를 기록한다.
2. **중단 실행:** 별도 실행에서 8번째 Epoch까지 동일하게 학습한 뒤 Checkpoint를 저장하고 프로그램을 종료한다. 중단과 재개는 **Epoch 경계** 에서만 발생하도록 한다.
3. **상태 보존:** `model_state`, `optimizer_state`, `scheduler_state`, `completed_epoch`, CPU RNG State, DataLoader Shuffle용 Generator State를 저장한다. Python·NumPy 난수를 실제로 사용했다면 그 상태도 포함한다.
4. **Early Stopping 상태:** 이번 고정 20 Epoch 비교에서는 중단 조건을 적용하지 않지만, 검증 Best Epoch와 Best Weight를 추적한다면 그것도 함께 저장·복원한다. Best 모델과 Resume State는 목적이 다름을 명시한다.
5. **정확한 재개:** Checkpoint를 불러와 Epoch 9부터 20까지 진행한다. 새 프로세스에서 모델·Optimizer·Scheduler를 생성한 뒤 각각의 State를 복원하며, 모델 생성에 사용된 난수가 재개 상태에 영향을 주지 않도록 **난수 State는 초기 구성 후 복원** 한다.
6. **결과 비교:** 연속 실행과 재개 실행의 마지막 Parameter(파라미터)별 최대 절댓값 차이 및 각 Epoch의 Loss·LR 차이를 비교한다. 같은 CPU·동일한 결정적 실행 조건에서 파라미터 차이는 `1e-6` 이하, LR 차이는 `1e-12` 이하여야 한다.
7. **안전한 저장:** 새 Checkpoint를 임시 파일에 완전히 기록한 뒤 원본 경로로 교체한다. 쓰기 실패가 발생하더라도 이전 정상 Checkpoint가 남아 있어야 한다. 파일 손상이 감지되면 불완전한 파일을 학습에 사용하지 않는다. 교체 이전의 정상 버전을 백업 파일로 보관하고, 복구 가능 여부와 실패 사유를 기록한다.
8. **복구 보고서:** 무엇이 잘못되었는지와 수정 전·후 결과의 차이를 정리한다. 동일한 결과를 얻지 못하는 환경에서는 원인을 기록하고 정확히 일치했다고 간주하지 않는다.

#### 입력 및 출력

프로그램은 `train.csv`, `validation.csv`와 선택적으로 저장된 `checkpoint.pt`를 사용합니다. `continuous`, `interrupt`, `resume`, `compare` 실행 모드를 제공하도록 구성할 수 있습니다.

- `continuous_history.csv`: `epoch,train_loss,validation_loss,learning_rate`
- `resumed_history.csv`: 같은 열 구조. 1~8 Epoch의 이전 기록과 재개 후 9~20 Epoch의 기록을 이어서 보존
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

위 값은 **출력 형식을 보여 주기 위한 예시**이며, 실제 측정 결과는 아닙니다.

<!-- 예시 결과 이미지 추가 예정 (정답 코드 실행 후 생성)
삽입 파일: ./assets/problems/c-01-resume-comparison.png
내용: 연속 학습과 중단·재개 학습의 Epoch별 Training Loss를 중첩한 그래프. 중단 지점(Epoch 8)과 실제 실행 결과 표시.
주의: 이미지를 평가용 필수 출력물로 간주하지 않음. 검증되지 않은 수치나 예시 결과를 임의로 만들지 말 것.
-->

#### 검증 기준

- 모델 Weight만 복원하거나 Scheduler State를 누락했을 때 차이가 발생하는 원인을 설명하는지 확인
- Shuffle과 Dropout의 난수가 정확히 이어지는지 확인
- Epoch 8까지의 기록을 재시작 시 덮어쓰지 않고 보존하는지 확인
- 잘못된 Checkpoint와 쓰기 실패 시 이전 정상 Checkpoint가 유지되는지 확인
- 정확한 Resume와 단순히 검증 성능이 비슷한 결과를 구분하는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 실행 상태와 실패 원인 분석</strong></summary>

연속 실행과 중단 후 재개 실행에서 학습 결과를 바꿀 수 있는 상태를 식별합니다. 저장 시점과 재개 시점의 차이를 분석합니다.

</details>

<details>
<summary><strong>STEP 2. 안전한 복구 절차 설계</strong></summary>

정확한 학습 재개에 필요한 상태를 관리하고, 파일 저장 중단이나 손상에도 이전 정상 상태를 보호할 수 있는 복구 흐름을 설계합니다.

</details>

<details>
<summary><strong>STEP 3. 재현성과 장애 대응 검증</strong></summary>

Epoch별 학습 이력과 최종 모델 상태를 비교합니다. 재현성 조건을 만족하지 못하면 원인을 기록하고 성공으로 처리하지 않습니다.

</details>

---

### C-02. 품질 판정 시스템의 예측 오류 대응

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Dtype · Device · [Chapter 06](../Chapter-06/README.md) · Model Inference · [Chapter 07](../Chapter-07/README.md) · Reproducibility · Model Handoff

#### 문제 설명

공장의 품질 판정 시스템은 안정적으로 운영되었지만, 입력 CSV를 생성하는 장비를 교체한 뒤 예측 점수가 급격히 달라졌습니다. 일부 측정값에는 숫자로 변환할 수 없는 문자열이 들어 있었고, Feature(특성) 열의 순서도 바뀌었습니다. 추론 코드가 평가 모드로 실행되지 않은 문제도 확인되었습니다.

아래 코드에는 서로 다른 종류의 위험이 섞여 있습니다.

```python
# 기존 코드 일부 — 결함 포함
incoming = pd.read_csv("incoming.csv")
x = torch.tensor(incoming.iloc[:, 1:].to_numpy(), dtype=torch.float32)
model.train()
probabilities = torch.sigmoid(model(x))
probabilities = probabilities.detach().numpy()
```

기존 코드와 기준 예측 기록을 비교하여 결과가 달라진 원인을 구분하십시오. 정상 입력에서도 발생하는 오류와 유효하지 않은 입력 때문에 생긴 실패를 별도로 분석합니다.

**목표는 예측 결과가 달라진 원인을 파악하고, 신뢰할 수 없는 예측이 자동 판정에 사용되지 않도록 복구 절차를 구현하는 것입니다.**

#### 제공 파일

- `model_weights.pt`: 신뢰 가능한 기준 모델의 Weight
- `preprocessing.json`: `feature_order`, `mean`, `scale`, `threshold`, `training_min`, `training_max` 저장
- `model_config.json`: 입력 차원, 모델 구조, 출력 차원, 모델 버전
- `reference_cases.csv`: 기준 모델로 검증한 입력 Sample(샘플)과 확률을 반올림 없이 저장한 파일 (복구 일치성 검사 전용; 확률 값은 최소 소수점 아홉째 자리까지 제공)
- `incoming.csv`: 운영 중 수신한 신규 데이터. `record_id`와 특성 열을 포함하지만 **열 순서는 달라질 수 있음**

특성 이름은 `temperature_c`, `vibration`, `hours_active`로 고정됩니다. 학습 범위의 최솟값과 최댓값은 학습 데이터에서 계산하며, 신규 입력에는 Target 정보가 없습니다.

#### 요구사항

1. **정확한 원인 분류:** 열 순서 변경, 숫자 형식 오류, Scaling 누락, `train()` 상태, 잘못된 Model(모델) Config를 각각 검증한다. 재현 로그를 남겨 어떤 문제로 예측이 달라졌는지 구분한다.
2. **Schema 검사:** `incoming.csv`에 `record_id`와 세 특성 열이 모두 있어야 한다. 추가 열은 무시할 수 있으나 필수 열이 하나라도 없으면 전체 추론을 중단하고 `SCHEMA_ERROR`를 기록한다.
3. **행별 유효성 검사:** `record_id`는 고유한 비어 있지 않은 문자열이어야 한다. 각 특성은 유한한 실수이고, `vibration`, `hours_active`는 0 이상이다. 무효 행은 `INVALID_VALUE`, 유효 ID 중복은 `DUPLICATE_ID`로 분리한다. 무효 행은 ID를 점유하지 않는다.
4. **정확한 복원:** 모델 설정과 Checkpoint의 Parameter(파라미터) Shape를 확인한다. `torch.load(..., map_location="cpu", weights_only=True)`로 읽고 특성은 **이름 기준**으로 정렬한다. 저장된 Scaling 기준을 적용하고 `eval()` + `torch.inference_mode()`에서 추론한다.
5. **기준 케이스 비교:** `reference_cases.csv`의 확률과 복원 모델의 확률을 반올림 전 값으로 비교한다. 최대 차이가 `1e-6`을 넘으면 운영 출력을 차단하고 원인을 기록한다.
6. **분포 변화 경보:** 신규 유효 행이 30개 이상일 때, 하나 이상의 특성 값이 **학습 Range 밖에 있는 행의 비율**을 계산한다. 비율이 20%를 초과하면 `SHIFT_ALERT`를 기록하고 해당 Batch의 자동 확정을 중단한다. 이 경보는 성능 저하의 증명이 아니라 추가 점검이 필요한 신호이다.
7. **안전한 출력:** Schema·모델 복원 오류나 기준 케이스 불일치가 발생하면 이전 정상 `predictions.csv`를 덮어쓰지 않는다. 유효한 추론 결과라도 `SHIFT_ALERT`가 발생하면 점수는 기록하되 상태를 `REVIEW_REQUIRED`로 지정하고 자동 확정은 하지 않는다.
8. **재현 및 복구:** 정상 입력, 열 순서가 바뀐 입력, 수치 오류, 분포 변화, 잘못된 모델 설정을 테스트하고 복구 전·후 차이를 기록한다.

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

유효하지 않은 행에 임의로 0이나 예측 Label을 채워 정상 결과처럼 기록해서는 안 됩니다.

#### 검증 기준

- 열 순서가 바뀌어도 결과가 같고, 필수 특성 누락은 정확히 탐지되는지 확인
- Scaling 누락, Mode 설정 오류, Checkpoint Shape 불일치를 서로 구분하는지 확인
- 신규 데이터에 Target이 없어도 Range 기반 경보를 계산할 수 있는지 확인
- `SHIFT_ALERT`가 발생했을 때 기존 점수와 자동 결정 정책을 혼동하지 않는지 확인
- 실패한 실행이 이전의 정상 결과 파일을 손상시키지 않는지 확인

#### HELP

<details>
<summary><strong>STEP 1. 장애 상황 재현과 원인 분리</strong></summary>

기준 입력과 장애가 발생한 입력으로 추론을 반복하여 차이를 확인합니다. 입력 형식, 모델 상태, 전처리 방식, 실행 환경 가운데 어디에서 문제가 발생했는지 구분합니다.

</details>

<details>
<summary><strong>STEP 2. 안전한 추론·복구 구조 설계</strong></summary>

정상 결과를 제공하기 전에 필수 검증을 완료하도록 구조를 설계합니다. 행별 오류와 전체 처리를 중단해야 하는 오류를 구분합니다.

</details>

<details>
<summary><strong>STEP 3. 운영 복귀 조건 검증</strong></summary>

기준 예측과의 일치성, 분포 변화 경보, 기존 결과 보존 여부를 확인합니다. 자동 판정을 다시 허용할 수 있는 조건을 검증합니다.

</details>

---
## Radiant

### R-01. The Last Checkpoint — AI 모델 운영과 장애 복구

**관련 개념:** [Chapter 05](../Chapter-05/README.md) · Tensor · Dataset · DataLoader · Autograd · [Chapter 06](../Chapter-06/README.md) · MLP · Binary·Regression Loss · Inference · [Chapter 07](../Chapter-07/README.md) · Optimizer · Scheduler · Early Stopping · Checkpoint · Reproducibility · Gradient Management

#### 문제 설명

여러 지역에 시설을 운영하는 회사가 설비 고장 위험과 다음 날의 전력 수요를 예측하는 시스템을 구축했습니다. 모델은 소규모 CPU 서버에서 주기적으로 학습되며, 학습이 완료되면 현장 시스템에서 새로운 예측 결과를 활용합니다.

그러나 실제 운영 과정에서 세 가지 문제가 확인되었습니다.

> 첫째, 학습 도중 전원이 차단되면 진행 상태를 복구하지 못해 처음부터 다시 학습해야 합니다.
> 
> 둘째, 새로운 모델을 배포한 뒤 예측 결과가 달라져도 어떤 데이터와 Weight가 사용되었는지 추적하기 어렵습니다.
> 
> 셋째, 기존보다 평가 점수가 높은 모델을 배포했지만 일부 사업장에서는 오히려 잘못된 경보가 증가하는 문제가 발생했습니다.

이러한 문제는 모델의 성능을 높이는 것만으로 해결할 수 없습니다. 학습 과정과 결과를 재현할 수 있어야 하며, 모델이 어떤 기준으로 평가되어 배포되었는지도 확인할 수 있어야 합니다. 또한, 문제가 발생했을 때 이전의 정상 상태로 돌아갈 수 있는 복구 체계도 필요합니다.

해당 프로젝트의 목표는 **모델의 학습과 검증, 배포 및 장애 복구를 안정적으로 수행할 수 있는 시스템을 구축하는 것**입니다. 단순히 높은 예측 성능을 달성하는 데 그치지 않고, 실제 운영 환경에서의 안정성과 처리 효율까지 고려해야 합니다.

다음 기능을 갖춘 Python 프로젝트를 설계하고 구현하십시오.

- 설비 고장 위험 Binary Classification
- 다음 날 전력 수요 Regression
- 중단된 학습의 정확한 재개
- 신규 사업장과 미래 데이터의 독립 평가
- 검증된 새 모델의 안전한 배포·복구
- 운영 데이터의 입력 오류와 분포 변화 감지
- Batch 추론의 처리 효율 분석

*해당 문제는 Chapter 05~07에서 학습한 PyTorch를 중심으로 해결할 수 있도록 구성되어 있습니다. CNN, Transformer, 분산 학습, 외부 클라우드 서비스 등의 기술은 요구하지 않습니다.*

#### 제공 데이터와 시점

모든 파일은 UTF-8 형식이고, 데이터는 실습용 합성 데이터입니다.

**1. `sites.csv` — 시설 기준 정보**

```csv
site_id,zone,capacity
S001,NORTH,200
S002,SOUTH,150
```

- `site_id`: 시설 고유 식별자
- `zone`: 운영 지역
- `capacity`: 1 이상의 정수, 모델 입력 Feature(특성)

**2. `history.csv` — 과거 관측값 및 사후 확정 Target**

```csv
site_id,date,temperature_c,vibration,energy_kwh,alarms_7d,failure_next_7d,energy_next_day,final_repair_cost
S001,2026-06-01,23,2.1,96,1,0,102,0
S002,2026-06-01,25,4.3,84,3,1,91,150000
```

| 열 | 의미 | 사용 기준 |
|---|---|---|
| `site_id`, `date` | 시설과 관측 날짜 | 연결·분할·중복 판단 |
| `temperature_c` | 당일 관측 기온 | 특성 |
| `vibration` | 당일 진동 값 | 특성, 0 이상 |
| `energy_kwh` | 당일 전력 사용량 | 특성, 0 이상 |
| `alarms_7d` | 관측 시점까지 최근 7일 경보 수 | 특성, 0 이상의 정수 |
| `capacity` | `sites.csv`에서 결합한 시설 수용 규모 | 특성 |
| `failure_next_7d` | 관측 이후 7일 동안 고장이 발생했는지 여부 | Classification Target 전용 |
| `energy_next_day` | 관측 다음 날의 확정 전력 수요 | Regression Target 전용 |
| `final_repair_cost` | 정비 후 확정된 수리비 | **특성 사용 금지** |

**3. `incoming.csv` — 운영 추론 대상**

```csv
site_id,date,temperature_c,vibration,energy_kwh,alarms_7d
S001,2026-09-01,24,2.4,105,1
S002,2026-09-01,26,4.7,89,4
```

Incoming 데이터에는 Target과 `final_repair_cost`가 없습니다. 관측이 종료된 시점에서 다음 날의 전력 수요와 이후 7일간의 고장 위험을 예측합니다.

**4. `deployment_manifest.json` — 현재 배포 중인 모델 정보**

최초 실행 시에는 배포된 모델이 없습니다. 따라서 이전 정상 버전이 확보된 이후에만 Rollback을 수행할 수 있습니다.

```json
{
  "active_version": null,
  "status": "EMPTY"
}
```

프로젝트에는 최소 10개 시설에 대해 아래 날짜 구간별로 충분한 기록이 제공됩니다. 학습·검증 데이터에는 두 클래스가 모두 존재합니다. Incoming에는 최소 30개 이상의 유효한 시설·날짜 기록이 포함된 기본 검증 세트가 제공됩니다.

#### 데이터 무결성과 처리 규칙

1. 모든 CSV는 헤더를 포함한다. `sites.csv`의 `site_id`는 고유해야 하며 `capacity`가 1 이상의 정수여야 한다. 시설 기준 파일의 오류는 전체 처리 중단 사유이다.
2. 과거·운영 데이터의 키는 `(site_id,date)`이다. 등록되지 않은 시설은 `UNKNOWN_SITE`, 잘못된 날짜는 `INVALID_DATE`, 누락 또는 비유한 숫자와 범위 오류는 `INVALID_VALUE`, 잘못된 Target은 `INVALID_TARGET`으로 기록한다.
3. 동일한 키를 가진 여러 기록 가운데 **첫 번째 유효한 행만 인정** 한다. 유효한 중복 기록은 `DUPLICATE_RECORD`로 거부한다. 앞선 무효 행은 키를 점유하지 않는다.
4. 오류 판정 우선순위는 `UNKNOWN_SITE` → `INVALID_DATE` → `INVALID_VALUE` → `INVALID_TARGET` → `DUPLICATE_RECORD`이다. Incoming에는 Target이 없으므로 `INVALID_TARGET` 검사를 적용하지 않는다.
5. `temperature_c`는 음수를 허용하지만 유한한 실수여야 한다. `vibration`·`energy_kwh`는 0 이상, `alarms_7d`는 0 이상의 정수이다. `failure_next_7d`는 0 또는 1, `energy_next_day`는 0 이상의 유한 실수이다.
6. 정합성 검사를 통과한 기록은 날짜 오름차순, 같은 날짜에서는 시설 ID 오름차순으로 정렬한다. 모든 오류 기록에는 `source_file`, 실제 파일 행 번호 `source_line`, `error_code`를 포함한다.
7. `final_repair_cost`는 사후 정보이므로 수치가 입력되어 있더라도 예측 특성, Scaling 기준 및 모델 선택 기준에 사용하지 않는다.

#### 요구사항

**STEP 01 — 데이터 준비와 검증**

- 세 CSV를 검사하고 정상 행과 거부 행을 분리한다.
- 학습에서 사용할 특성 목록을 `[temperature_c, vibration, energy_kwh, alarms_7d, capacity]`로 고정한다.
- 모든 특성의 Scaling 기준은 학습 데이터에서만 계산한다. 표준편차가 0인 특성은 Scale을 1로 처리한다.
- 정상·오류 행의 개수, 시설 수, 날짜 범위와 오류 코드별 건수를 기록한다.
- 데이터 검증에 실패해 학습할 수 없다면 이전에 배포한 모델과 결과를 손상시키지 않는다.

**STEP 02 — 시간 구간과 신규 시설 분리**

날짜 기준은 다음과 같이 고정한다.

| 구간 | 기록 날짜 | 용도 |
|---|---|---|
| 학습 | 2026-03-01 ~ 2026-06-30 | 학습·전처리 기준 |
| Gap 1 | 2026-07-01 ~ 2026-07-07 | 평가 대상에서 제외 |
| 검증 | 2026-07-08 ~ 2026-07-21 | Best Weight·Threshold·배포 후보 비교 |
| Gap 2 | 2026-07-22 ~ 2026-07-28 | 평가 대상에서 제외 |
| Test(테스트) | 2026-07-29 ~ 2026-08-11 | 독립적인 최종 평가 |

고장 여부의 Target은 관측 이후 7일간 발생한 사건을 나타내므로, 구간 사이에 7일의 Gap을 둔다. Gap은 학습·모델 선택·점수 계산에 포함하지 않는다. 운영 추론 날짜는 `2026-09-01` 이후이며, 테스트 Target이 확정된 뒤에 배포 평가가 진행된다고 가정한다.

추가로 학습하지 않은 시설에 대한 일반화 성능도 평가한다.

- 고유 `site_id`를 문자열 오름차순으로 정렬한 뒤 **5번째, 10번째, 15번째 …** 시설을 Holdout으로 지정한다.
- Holdout 시설의 모든 기록은 학습·검증과 Scaling에 사용하지 않는다.
- **평가 A:** Holdout이 아닌 시설의 테스트 기간 기록
- **평가 B:** Holdout 시설의 테스트 기간 기록

평가 A와 B의 결과를 따로 기록한다. Holdout 시설의 Target을 사용해 모델·Threshold·배포 후보를 선택하지 않는다.

**STEP 03 — 두 종류의 MLP 구성 및 학습**

Classification과 Regression을 서로 독립적인 모델로 구성한다. 공통 입력은 5개 특성이다.

| 구분 | Model(모델) 구조 | Loss | 주요 Metric |
|---|---|---|---|
| Classification | `Linear(5,16) → ReLU → Linear(16,1)` | `BCEWithLogitsLoss` | Recall, F2, Precision |
| Regression | `Linear(5,16) → ReLU → Linear(16,1)` | `MSELoss` | MAE, RMSE |

- 두 모델 모두 Dataset·DataLoader를 사용하며 CPU에서 실행하는 것을 기본으로 한다.
- 1개 Batch는 최대 32개 Sample(샘플)을 포함하고 마지막 Batch를 버리지 않는다.
- 학습 Loss는 Batch별 단순 평균이 아니라 샘플 수를 반영해 집계한다.
- Gradient 초기화는 매 Optimizer Update 전에 수행한다.
- Classification의 Baseline은 학습 다수 클래스를 예측하는 모델이며, Regression Baseline은 당일 `energy_kwh`를 그대로 예측하는 방법이다.

**STEP 04 — 배포 버전별 학습과 중단 복구**

모델 버전을 두 단계로 구성한다.

- **v1:** `SGD(lr=0.02, momentum=0.9)`, 최대 24 Epoch
- **v2:** `AdamW(lr=0.005, weight_decay=0.01)`, 최대 24 Epoch

두 버전은 모델 구조와 초기 Seed 42, DataLoader의 샘플 순서, 학습·검증 데이터를 동일하게 맞춘다. 단, Optimizer 설정이 다르므로 같은 학습 궤적이나 같은 성능을 기대하는 것은 아니다.

v2 학습에는 `StepLR(step_size=8,gamma=0.5)`를 적용한다. 검증 Metric이 개선된 Best Weight를 보관하고 Early Stopping Patience 6을 적용하되, **최소 8 Epoch를 완료한 뒤부터** 중단 조건을 허용한다. v1·v2의 최고 검증 기준은 Classification에서는 F2, Regression에서는 RMSE이다. Classification은 각 Epoch에서 검증의 `[0.30,0.50,0.70]`을 모두 평가하여 F2가 가장 높은 Weight·Threshold 조합을 Best로 보관한다. F2 동점이면 높은 Threshold, 그래도 같으면 이른 Epoch를 선택한다.

v2는 **6번째 Epoch 종료 직후 의도적으로 중단하고 새 프로세스에서 재개** 해야 한다. Checkpoint에는 최소한 다음 상태가 포함되어야 한다.

- 모델·Optimizer·Scheduler State
- 완료한 Epoch, Best 검증 Metric·Best Weight, Early Stopping Counter
- Torch RNG State와 Shuffle용 Generator State
- 학습에 영향을 준 Config·특성 순서·Scaling 기준의 식별 정보

연속 실행과 중단·재개 실행을 동일한 CPU·입력·환경에서 비교하여 최종 Parameter(파라미터)의 최대 절댓값 차이가 `1e-6` 이하인지 검사한다. 저장은 임시 파일 작성 후 원자적 교체를 사용한다.

**STEP 05 — 검증 기반 배포 후보 선택**

v1과 v2를 **검증에서만** 비교한다. 배포 승격 규칙을 다음과 같이 고정한다.

1. v2의 Classification 검증 F2가 v1보다 낮아서는 안 된다.
2. v2의 Regression 검증 RMSE가 v1보다 높아서는 안 된다.
3. 두 조건을 충족하며 적어도 하나의 지표가 엄격하게 개선되어야 v2를 승격한다.
4. 이 조건을 만족하지 않으면 v1을 유지한다.

비교는 반올림 전 값으로 수행한다. 선정이 끝나면 **확정한 버전의 두 모델**로만 평가 A·B의 테스트 점수를 계산한다. 테스트 성능을 기준으로 승격 결정을 바꾸지 않는다.

**STEP 06 — 운영 추론과 경보 처리**

- `incoming.csv`의 특성을 저장된 이름·순서와 Scaling 기준으로 변환한다.
- `eval()`과 `torch.inference_mode()`에서 Classification 확률과 Regression 예측값을 계산한다.
- Classification의 확률이 선정된 Threshold 이상인 기록을 점검 후보로 정한다.
- **지역(`zone`)·날짜별 최대 3개 시설**을 확률 내림차순으로 선정한다. 확률이 같으면 시설 ID 오름차순을 적용한다. 나머지는 `BELOW_THRESHOLD` 또는 `CAPACITY_LIMIT`로 표시한다.
- 신규 입력에서 한 행이라도 누락값이나 범위 오류가 있으면 해당 행을 거부하며, 유효한 나머지 기록은 별도로 처리한다.

**STEP 07 — 분포 변화 경보와 안전한 배포**

- 학습에서 특성별 관측 최소·최댓값을 함께 저장한다.
- Incoming에서 유효 행이 30개 이상이면, 하나 이상의 특성값이 학습 Range 밖에 있는 행의 비율을 구한다.
- 해당 비율이 20%를 초과하면 `SHIFT_ALERT`를 기록하고 자동 점검 대상 확정을 중단한다. 예측 점수는 확인용으로 남길 수 있지만 `REVIEW_REQUIRED`로 구분한다.
- 새 모델의 학습·검증과 Incoming 추론을 모두 통과한 뒤에만 배포 버전 정보를 갱신한다. 배포 정보 파일은 마지막에 교체한다.
- 모델 파일 손상, Loader 예외, 기준 예측값 불일치 또는 결과 저장 실패가 발생하면 이전 정상 버전의 Weight·전처리 기준·결과를 유지해야 한다.
- 배포 이후 문제가 확인되면 보존된 이전 정상 버전으로 Rollback할 수 있어야 한다. 이전 정상 버전이 없는 상태에서 Rollback을 요청하면 `NO_ROLLBACK_TARGET`을 기록한다. 배포 버전의 변경 이력은 별도로 관리한다.

**STEP 08 — 추론 최적화 및 결과 일치 검증**

- 검증 가능한 기준 구현(행별 추론)과 Batch 단위 Tensor(텐서) 추론을 각각 실행한다.
- 동일한 입력에 대해 Classification 확률과 Regression 예측값의 최대 절댓값 차이가 `1e-6` 이하인지 확인한다.
- 동일 CPU에서 여러 번 실행한 처리 시간을 측정하고 중앙값을 기록한다. 환경에 따라 시간 차이가 달라지므로 특정 속도 향상을 요구하지 않는다.
- 추론 속도가 개선되어도 행 순서, 예측값, 상태 코드, 경보 목록이 바뀌지 않아야 한다.

#### 입력 및 출력 규격

프로젝트는 `validate`, `train`, `resume`, `evaluate`, `predict`, `promote`, `rollback`, `benchmark` 등 단계별 명령으로 실행할 수 있습니다. 코드 구조는 자유롭게 설계하되, 각 단계에서 필요한 이전 단계의 산출물이 준비되었는지 확인해야 합니다.

**필수 결과물**

| 파일 | 내용 |
|---|---|
| `clean_history.csv` | 정상 과거 기록, 날짜·시설 ID 순으로 정렬 |
| `rejected_rows.csv` | `source_file,source_line,error_code` |
| `data_audit.json` | 유효·무효 행 수, 오류 코드, 분할 날짜, Holdout Site 목록 |
| `training_history.csv` | `version,task,epoch,train_loss,validation_metric,learning_rate` |
| `checkpoints/` | v2의 중단·재개 학습 상태, Best Weight |
| `resume_audit.json` | 연속 실행과 재개 실행의 파라미터 차이, 성공 여부 |
| `validation_selection.json` | v1·v2 검증 지표와 배포 후보 선택 이유 |
| `test_evaluation.json` | 평가 A·B의 Classification·Regression 지표와 Baseline 비교 |
| `deployment_manifest.json` | 현재 버전, 모델·전처리 파일 경로, 검증 상태 |
| `incoming_predictions.csv` | `site_id,date,failure_probability,energy_prediction,selected,status` |
| `shift_report.json` | 유효 행 수, 범위 초과 비율, `SHIFT_ALERT`, 자동 확정 가능 여부 |
| `benchmark.json` | 행별·Batch 추론 시간 중앙값, 결과 최대 차이 |
| `final_report.md` | 실험 설계, 복구·배포 이력, 테스트 평가, 오류 분석 및 성능 비교 |

Classification 평가에는 Accuracy뿐 아니라 Precision·Recall·F2·Confusion Matrix도 포함해야 합니다. Regression에는 MAE와 RMSE를 함께 기록하며, 테스트 예측값의 오차가 큰 사례도 분석합니다. 수치 파일에는 소수점 넷째 자리까지 기록할 수 있지만, 모든 비교와 경보 판정은 반올림 전 값으로 수행합니다.

<!-- 예시 결과 이미지 추가 예정 (정답 코드 실행 후 생성)
삽입 파일: ./assets/problems/r-01-deployment-evaluation.png
내용: 검증 데이터에서 선택된 버전의 분류 F2와 회귀 RMSE를 비교한 그래프. 실행 결과와 단위·버전 식별 정보를 명시.
주의: 이미지를 평가용 필수 출력물로 간주하지 않음. 검증되지 않은 수치나 예시 결과를 임의로 만들지 말 것.
-->

#### 공개 검증 예제 — 무효 행과 중복 처리

다음은 Schema 검사 후 정상 행을 선택하는 규칙을 보여 주는 예시입니다. 전체 모델을 학습하기 위한 데이터 규모는 아닙니다.

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

`S001`의 첫 번째 유효 기록만 인정합니다. `S002`의 음수 진동 기록은 무효이므로 같은 키를 점유하지 않으며, 그다음 유효 기록을 정상 처리합니다.

#### 최종 검증 기준

1. **구조와 수식:** 텐서 Shape, Logit·Target Shape, Loss와 학습 Loop가 의도한 대로 작동하는지 확인
2. **데이터 무결성:** 무효 행이 학습·평가·운영 출력에 섞이지 않고 오류 사유를 추적할 수 있는지 확인
3. **미래 정보 차단:** 사후 수리비와 미래 Target이 특성에 들어가지 않으며, 날짜 Gap과 Holdout 구분이 지켜지는지 확인
4. **정확한 복구:** Optimizer·Scheduler·난수 상태를 포함한 Resume이 연속 실행 결과와 일치하는지 확인
5. **독립적인 평가:** 검증으로 확정한 모델·Threshold를 테스트에서 변경하지 않는지 확인
6. **안전한 운영 정책:** 지역별 점검 한도, 동점 처리, Shift 경보와 자동 처리 차단이 정확한지 확인
7. **배포·복구:** 새 버전 실패 시 이전 정상 Weight·전처리·결과가 남고 Rollback이 가능한지 확인
8. **재현성:** 동일한 입력·설정에서 파일 순서와 결정적 판단 결과가 일치하는지 확인
9. **최적화:** 더 빠른 추론 구현이 결과를 바꾸지 않으며, 시간 측정 조건을 명확히 기록했는지 확인

#### 제출 결과물

실행 가능한 Python 프로그램, 실습용 합성 데이터, 결과 파일, 자동 검증 코드와 최종 보고서를 제출한다. 코드의 폴더 구조는 자유롭게 설계할 수 있으나, 데이터 검사부터 학습·복구·평가·배포·Rollback까지 각 단계의 입력과 출력이 명확해야 한다.

#### HELP

<details>
<summary><strong>STEP 1. 데이터 계약과 정합성</strong></summary>

필수 열·허용 범위·키 중복·오류 우선순위를 먼저 정의합니다. 학습 모듈이 검증된 입력만 받도록 데이터 처리의 경계를 정합니다.

</details>

<details>
<summary><strong>STEP 2. 두 예측 작업의 책임 분리</strong></summary>

Classification과 Regression의 입력 처리 방식은 공유할 수 있으나, 모델 상태·Loss·Optimizer·선택 지표를 독립적으로 관리합니다.

</details>

<details>
<summary><strong>STEP 3. 학습과 모델 선택 구조</strong></summary>

Epoch별 이력과 Best Weight를 재현 가능하게 기록합니다. 가중치 선택과 Threshold 선택의 순서를 명확히 분리합니다.

</details>

<details>
<summary><strong>STEP 4. 중단 복구 검증</strong></summary>

중단·재개 결과가 연속 실행과 일치하지 않는다면 신규 버전을 배포 후보로 등록하지 않습니다. 초기화·Shuffle·저장 시점과 복원 시점의 영향을 점검합니다.

</details>

<details>
<summary><strong>STEP 5. 검증과 테스트의 역할 분리</strong></summary>

검증 데이터를 기준으로 모델 버전과 Threshold를 확정합니다. 테스트 데이터는 최종 성능 평가에만 사용하며, 평가 결과에 따라 기존 선택을 변경하지 않습니다.

</details>

<details>
<summary><strong>STEP 6. 추론 입력과 운영 정책</strong></summary>

배포 버전마다 입력 특성 순서, Scaling, 모델 파일과 경보 정책을 함께 관리합니다. 거부된 입력이 정상 예측이나 운영 우선순위에 섞이지 않도록 합니다.

</details>

<details>
<summary><strong>STEP 7. 배포·Rollback의 원자성</strong></summary>

버전별 산출물을 독립적으로 보관하고 검증한 뒤 활성 버전 정보를 마지막에 교체합니다. 배포 이력이 없는 최초 실행과 이전 정상 버전이 있는 운영 상태를 구분합니다.

</details>

<details>
<summary><strong>STEP 8. 검증 가능한 최적화</strong></summary>

정상 동작하는 기준 구현을 먼저 확보합니다. Batch 추론의 속도를 측정하되, 처리 순서와 결과·상태 코드가 달라지지 않았음을 검증합니다.

</details>

---

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)
