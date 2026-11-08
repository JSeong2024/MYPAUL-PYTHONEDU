# Problems — Summary Part 01

Chapter 01~04 · **Basic 5 · Advanced 4 · Professional 3 · Challenge 2 · Radiant 1**

각 문제의 입력·출력 조건을 충족하는 Python 프로그램을 작성하시오. 예제는 공개된 검증 사례이며, 예제만 통과하는 코드는 완성된 구현으로 간주하지 않습니다. 관련 개념과 구현 가이드는 필요할 때 확인할 수 있습니다.

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)

## Basic

### B-01. Feature & Target Inspector — 데이터 구조 및 정합성 검사

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Sample · Feature · Target · Array Shape · Data Validation

#### 문제 설명

머신러닝 파이프라인을 구축할 때 가장 먼저 선행되어야 할 작업은 입력 데이터의 구조와 무결성을 검증하는 것입니다. 학습 데이터의 행(Sample)과 열(Feature/Target)이 올바르게 구성되었는지 사전에 확인하지 않으면, 차원 불일치 오류나 잘못된 레이블로 인해 학습 과정에서 치명적인 문제가 발생할 수 있습니다.

본 문제에서는 첫 줄에 샘플 수와 특성 수가 주어지고, 이어지는 행들에 각 샘플의 특성 값들과 이진 분류용 타겟 레이블이 공백으로 구분되어 입력됩니다. 전체 데이터의 구조를 안전하게 파싱하고 유효성을 검사하여 요약 정보를 출력하는 프로그램을 작성하시오.

#### 요구 사항

1. 첫 줄에서 샘플 수 `N`과 특성 수 `D`를 읽은 뒤, 이어지는 `N`개 행에서 `D`개의 Feature와 1개의 Target을 각각 분리합니다.
2. 독립 변수 `X`의 배열 Shape는 `(N, D)`, 타겟 `y`의 Shape는 `(N,)`으로 올바르게 구성합니다.
3. 타겟 값인 `0`과 `1`의 빈도수를 각각 정확히 집계합니다.
4. 각 행의 데이터 개수가 일치하지 않거나, Target 값이 `0` 또는 `1` 이외의 정수일 경우 `INVALID`를 출력합니다.

#### 입력

첫 줄에 샘플 수 `N`과 특성 수 `D`가 공백으로 구분되어 주어집니다. 이어지는 `N`개 줄에는 실수 형태의 Feature `D`개와 정수 형태의 Target 1개가 공백으로 구분되어 입력됩니다.

- `1 ≤ N ≤ 1,000`, `1 ≤ D ≤ 20`
- Feature 값은 유한한 실수이며, Target 값은 `0` 또는 `1`입니다.

#### 출력

데이터가 유효한 경우, 샘플 수, 특성 수, 그리고 각 타겟별 빈도수를 아래의 정해진 형식에 맞춰 출력합니다. 입력 형식이 잘못되었거나 유효성 검증을 통과하지 못한 경우 `INVALID`를 한 줄에 출력합니다.

**예제 입력**

```text
3 2
1.5 2.0 0
2.1 3.0 1
1.2 2.8 0
```

**예제 출력**

```text
SAMPLES 3
FEATURES 2
TARGET_0 2
TARGET_1 1
```

#### 검증 항목 (Edge Cases)

- **경계값 조건:** `N = 1` 또는 `D = 1`인 최소 크기 입력에서도 배열의 차원(Shape)이 깨지지 않고 올바르게 유지되는지 확인
- **결측 및 초과 데이터:** Feature의 개수가 부족하거나 초과하는 경우, 또는 유효하지 않은 문자열이나 공백 예외 처리
- **타겟 유효성 및 편향:** Target 값이 `0` 또는 `1` 범위를 벗어나는 경우, 혹은 데이터셋 전체의 Target이 모두 `0`이거나 모두 `1`로 편향된 경우에도 집계가 정상적으로 수행되는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

1. **데이터 파싱 및 길이 검증:** 입력받은 각 행을 공백으로 분리하여, 리스트의 전체 길이가 정확히 `D + 1`(`Feature` `D`개 + `Target` 1개)인지 먼저 검증합니다.
2. **배열 분리 및 변환:** 검증된 데이터에서 마지막 원소를 `Target`(`y`)으로, 앞의 `D`개 원소를 `Feature`(`X`)로 분리한 뒤 각각 적절한 타입의 NumPy 배열(`np.float64`, `np.int64`)로 변환합니다.
3. **구조 및 통계 점검:** 생성된 배열의 `X.shape`, `y.shape`가 각각 `(N, D)`, `(N,)` 형태를 만족하는지 확인하고, 조건에 맞지 않거나 예외가 발생할 경우 즉시 `INVALID`를 출력하도록 처리합니다.

</details>

---

### B-02. Prediction Error Calculator — 회귀 예측 모델과 기준 모델(Baseline)의 오차 비교

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Linear Regression · MAE · MSE · Baseline Model · Evaluation

#### 문제 설명

회귀(Regression) 모델의 성능을 평가할 때는 복잡한 알고리즘이 예측한 결과가 단순한 기준 모델(Baseline)에 비해 얼마나 더 우수한지 비교하는 것이 중요합니다. 

본 문제에서는 파라미터 `w`와 `b`가 주어지는 단순 선형 회귀 모델($\hat{y} = wx + b$)과, 훈련 타겟의 평균값을 모든 샘플의 예측값으로 사용하는 기준 모델(Baseline)을 각각 설정합니다. 주어진 테스트 데이터셋에 대해 두 모델의 **평균 절대 오차(MAE, Mean Absolute Error)** 를 각각 계산하고, 더 우수한(즉, MAE가 더 작은) 예측 방식을 판별하여 출력하는 프로그램을 작성하시오.

#### 요구 사항

1. **Baseline 설정:** 입력된 Training Target의 평균값을 계산하여 기준 모델(Baseline)의 예측 상수로 설정합니다. (※ 테스트 타겟이 아닌 훈련 타겟의 평균을 사용함에 유의)
2. **회귀 모델 평가:** 주어진 파라미터 `w`, `b`를 바탕으로 Test Sample에 대한 예측값 $\hat{y} = wx + b$를 계산하고, 모델의 **MAE(Mean Absolute Error)**와 **MSE(Mean Squared Error)**를 각각 산출합니다.
3. **Baseline 평가:** 동일한 Test Sample에 대해 훈련 타겟 평균값으로 예측을 수행하고, 이에 대한 Baseline의 **MAE**를 계산합니다.
4. **성능 비교 및 판정:** 두 모델의 MAE를 비교하여 회귀 모델의 오차가 더 작으면 `MODEL`, Baseline의 오차가 더 작으면 `BASELINE`, 두 오차가 정확히 같으면 `TIE`를 출력합니다.

#### 입력

- 첫 번째 줄: 회귀 모델의 파라미터 `w`와 `b`가 공백으로 주어집니다.
- 두 번째 줄: 훈련 타겟의 개수 `K`가 주어집니다.
- 세 번째 줄: `K`개의 훈련 타겟 값들이 공백으로 주어집니다.
- 네 번째 줄: 테스트 샘플의 수 `N`이 주어집니다.
- 다섯 번째 줄부터 `N`개 줄: 각 테스트 샘플의 특성값 `x`와 실제 타겟값 `y`가 공백으로 주어집니다.

- `1 ≤ K, N ≤ 1,000`
- 모든 입력값은 유한한 실수입니다.

#### 출력

계산된 `MODEL_MAE`, `MODEL_MSE`, `BASELINE_MAE` 및 최종 비교 결과(`BEST`)를 소수점 넷째 자리까지 반올림하여 아래 형식으로 출력합니다.

**예제 입력**

```text
2 1
2
2 4
3
1 3
2 6
3 7
```

**예제 출력**

```text
MODEL_MAE 0.3333
MODEL_MSE 0.3333
BASELINE_MAE 2.3333
BEST MODEL
```

#### 검증 항목 (Edge Cases)

- **완벽한 예측 (Zero Residual):** 모델의 예측값이 실제 값과 완전히 일치하여 Residual이 모두 `0`인 경우의 MAE 및 MSE 계산 처리
- **단일 샘플 예외 (K=1):** 훈련 타겟의 개수가 `K = 1`일 때 단일 값의 평균 계산이 예외 없이 정상 동작하는지 확인
- **오차 부호 처리:** 음수 오차가 발생했을 때 MAE는 절댓값을 올바르게 반영하고, MSE는 제곱 연산을 통해 양수로 변환되는지 확인
- **데이터 독립성 (Data Leakage 방지):** Baseline 예측값 산출 시 오직 훈련 타겟의 평균만 사용되며, 테스트 타겟 데이터가 섞이지 않았는지 엄격하게 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **Baseline 기준 상수 산출:** 입력된 훈련 타겟 전체의 평균값을 구하여 기준 모델의 고정 예측값으로 설정합니다. (예: 훈련 타겟이 `[2, 4]`인 경우 평균은 `3.0`)
2. **회귀 모델 오차 계산:** 테스트 샘플의 특성 `x`에 대해 $\hat{y} = wx + b$를 계산한 뒤, 실제 테스트 타겟 `y`와 비교하여 MAE와 MSE를 산출합니다. 
   - (예: 모델 예측값이 `[3, 5, 7]`이고 실제 값이 `[3, 6, 7]`일 때, 절댓값 오차의 평균인 MAE와 제곱 오차의 평균인 MSE를 각각 계산)
3. **지표 분모 설정:** MAE와 MSE의 평균을 계산할 때의 분모는 훈련 샘플 수 `K`가 아닌 **테스트 샘플 수 `N`**을 사용해야 함에 유의합니다.
4. **결과 비교 및 출력:** 회귀 모델의 MAE와 Baseline의 MAE를 소수점 넷째 자리까지 정확하게 반올림하여 비교한 뒤 규격에 맞춰 출력합니다.

</details>

---

### B-03. First Gradient Update — 첫 번째 파라미터 갱신 및 예측

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Loss Function · Partial Derivative · Gradient Descent · Optimization

#### 문제 설명

선형 모델 $\hat{y} = wx + b$의 예측 오차를 줄이기 위해 경사하강법(Gradient Descent)을 적용하여 파라미터를 단 한 번 갱신(Update)하고, 갱신된 파라미터로 새로운 예측값을 산출하고자 합니다. 단일 샘플 $(x, y)$에 대한 손실 함수(Loss Function)는 다음과 같이 정의됩니다.

$$L = \frac{1}{2}(wx + b - y)^2$$

주어진 단일 샘플, 초기 파라미터($w$, $b$), 그리고 학습률(Learning Rate, $\eta$)을 활용하여 편미분을 통해 기울기(Gradient)를 계산하고, 갱신된 파라미터와 새로운 예측값을 출력하는 프로그램을 작성하시오.

#### 요구 사항

1. **오차 계산:** 예측 오차 $e = wx + b - y$ (또는 $\hat{y} - y$)를 계산합니다.
2. **기울기(Gradient) 산출:** 손실 함수의 편미분 공식을 이용해 각 파라미터의 기울기를 구합니다.
   - $\frac{\partial L}{\partial w} = e \cdot x$
   - $\frac{\partial L}{\partial b} = e$
3. **파라미터 갱신:** 학습률 $\eta$를 반영하여 경사하강법 공식을 통해 새로운 파라미터를 계산합니다.
   - $w_{\text{new}} = w - \eta \cdot \frac{\partial L}{\partial w}$
   - $b_{\text{new}} = b - \eta \cdot \frac{\partial L}{\partial b}$
4. **신규 예측값 산출:** 갱신된 파라미터($w_{\text{new}}$, $b_{\text{new}}$)를 바탕으로 동일한 입력 $x$에 대한 새로운 예측값($\hat{y}_{\text{new}} = w_{\text{new}}x + b_{\text{new}}$)을 구합니다.

#### 입력

한 줄에 특성 `x`, 실제 타겟 `y`, 초기 파력미터 `w`, `b`, 그리고 학습률 `eta`가 공백으로 구분되어 주어집니다.

- 모든 수는 유한한 실수입니다.
- 학습률 조건: `0 < eta ≤ 1`

#### 출력

계산된 `GRAD_W`, `GRAD_B`, `NEW_W`, `NEW_B`, 그리고 `PREDICTION` 값을 소수점 넷째 자리까지 반올림하여 출력합니다.

**예제 입력**

```text
2 5 1 0 0.1
```

**예제 출력**

```text
GRAD_W -6.0000
GRAD_B -3.0000
NEW_W 1.6000
NEW_B 0.3000
PREDICTION 3.5000
```

#### 검증 항목 (Edge Cases)

- **무변동 조건:** 예측 오차가 `0`인 경우 기울기(Gradient)가 `0`이 되어 파라미터가 변경되지 않고 기존 값을 그대로 유지하는지 확인
- **음수 Gradient 방향성:** 기울기가 음수일 때, 경사하강법 공식에 의해 파라미터가 올바른 방향(증가하는 방향)으로 갱신되는지 확인
- **계수 상쇄 효과:** 손실 함수 정의에 포함된 $\frac{1}{2}$ 계수가 편미분 과정에서 지수 `2`와 곱해져 자연스럽게 소거(`1`)되는지 수학적 정합성 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **동시 계산 원칙:** 미분을 수행하기 전의 초기 파라미터(`w`, `b`)를 기준으로 $w$와 $b$의 기울기를 각각 독립적으로 계산하세요.
2. **동기화 유지:** 기울기를 구하는 과정에서 $w$를 먼저 변경해버리면 $b$의 기울기 계산 시점에 영향을 주어 잘못된 결과가 산출될 수 있으므로, 두 기울기를 모두 구한 뒤 한꺼번에 갱신하세요.
3. **단계별 적용:** 갱신이 완료된 새로운 $w_{\text{new}}$와 $b_{\text{new}}$는 최종 단계에서 새로운 예측값(`PREDICTION`)을 산출할 때만 사용해야 합니다.

</details>

---

### B-04. Classification Metrics — 이진 분류 결과 및 성능 지표 분석

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Decision Threshold · [Chapter 04](../Chapter-04/README.md) · Confusion Matrix · Precision · Recall · F1-Score

#### 문제 설명

이진 분류 모델이 산출한 예측 확률(또는 점수)에 결정 임계값(Decision Threshold)을 적용하여 최종 예측 레이블을 결정하고자 합니다. 주어진 임계값을 기준으로 예측 레이블을 생성한 뒤, 실제 레이블과 비교하여 혼동 행렬(Confusion Matrix)의 구성 요소를 도출하고 주요 분류 평가 지표를 계산하는 프로그램을 작성하시오.

#### 요구 사항

1. **임계값 적용:** 각 샘플의 예측 점수(`score`)가 임계값(`threshold`) 이상(`score >= threshold`)이면 양성(`1`), 그렇지 않으면 음성(`0`)으로 예측 레이블을 결정합니다.
2. **혼동 행렬 산출:** 실제 레이블(`actual`)과 예측 레이블을 비교하여 `TP`(True Positive), `FP`(False Positive), `FN`(False Negative), `TN`(True Negative)의 개수를 각각 정확히 계산합니다.
3. **성능 지표 계산:** 정밀도(Precision), 재현율(Recall), 그리고 두 지표의 조화 평균인 F1-Score를 계산합니다.
4. **분모 0 예외 처리:** Precision 또는 Recall 계산 시 분모가 `0`이 되는 상황(예: 양성 예측 개수가 0이거나 실제 양성 개수가 0인 경우)이 발생하면, 해당 지표의 값은 경고나 에러 없이 **`0.0000`**으로 대체하여 출력합니다.

#### 입력

- 첫 번째 줄: 전체 샘플 수 `N`과 결정 임계값 `threshold`가 공백으로 주어집니다.
- 두 번째 줄부터 `N`개 줄: 각 샘플의 실제 레이블 `actual`과 예측 점수 `score`가 공백으로 구분되어 주어집니다.

- `1 ≤ N ≤ 10,000`, `0 ≤ threshold ≤ 1`
- `actual` 값은 `0` 또는 `1`, `score` 값은 `0 이상 1 이하`의 실수입니다.

#### 출력

혼동 행렬 지표인 `TP`, `FP`, `FN`, `TN`을 정수 형태로 출력하고, 이어지는 세 가지 성능 지표(`Precision`, `Recall`, `F1-Score`)를 소수점 넷째 자리까지 반올림하여 출력합니다.

**예제 입력**

```text
5 0.5
0 0.10
1 0.80
1 0.40
0 0.60
1 0.90
```

**예제 출력**

```text
TP 2
FP 1
FN 1
TN 1
PRECISION 0.6667
RECALL 0.6667
F1 0.6667
```

#### 검증 항목 (Edge Cases)

- **경계값 일치 (`Score == Threshold`):** 예측 점수가 임계값과 정확히 일치하는 샘플들이 조건식(`>=`)에 따라 올바르게 양성(`1`)으로 분류되는지 확인
- **제로 디비전 및 극한 상황:** 양성 예측이 전혀 없는 경우(`TP + FP = 0`), 실제 양성이 전혀 없는 경우(`TP + FN = 0`), 혹은 데이터셋 전체에 단 하나의 클래스만 등장하는 입력에서도 프로그램이 중단되지 않고 안정적으로 동작하는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

1. **혼동 행렬 선집계:** 임계값 비교를 통해 예측 레이블을 먼저 확정한 뒤, `TP`, `FP`, `FN`, `TN`의 네 가지 분류 결과를 완벽하게 먼저 집계합니다.
2. **안전한 지표 함수 분리:** 각 지표의 분모가 `0`인지 사전에 검사하는 전용 함수(또는 안전 나눗셈 로직)를 별도로 구현하여 런타임 오류를 방지하세요.
3. **F1-Score 통합 계산식 활용:** 수식 변형 형태인 $F_1 = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$ 공식을 활용하면, Precision과 Recall이 모두 0이 되는 예외 상황에서도 분모 조건 처리를 일관되고 간결하게 수행할 수 있습니다.
4. **출력 포맷팅:** 정수는 정수형으로, 소수점 지표들은 `round(val, 4)` 또는 `{:.4f}` 포맷을 적용하여 소수점 넷째 자리까지 정확하게 출력합니다.

</details>

---

### B-05. KMeans Assignment — 클러스터 중심 할당 및 갱신

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · Euclidean Distance · Centroid Update · Cluster Assignment

#### 문제 설명

KMeans 클러스터링 알고리즘의 핵심 단계인 **'데이터 할당(Assignment)'** 과 **'중심점 갱신(Centroid Update)'** 과정을 직접 구현하고자 합니다. 2차원 공간 상의 초기 중심점 두 개와 샘플들이 주어졌을 때, 각 샘플을 더 가까운 중심에 할당하고, 새롭게 구성된 클러스터의 평균 좌표를 바탕으로 중심점을 단 한 번 갱신하는 프로그램을 작성하시오.

#### 요구 사항

1. **유클리드 거리 계산:** 각 샘플과 두 초기 중심($C_0, C_1$) 사이의 유클리드 거리(Euclidean Distance)를 각각 계산합니다.
2. **동점 처리 규칙:** 두 중심까지의 거리가 정확히 같다면 **인덱스가 더 작은 중심(클러스터 0)**에 우선적으로 할당합니다.
3. **중심점 갱신:** 각 클러스터(Cluster 0, Cluster 1)에 할당된 샘플들의 좌표별 평균(Mean)을 산출하여 새로운 중심 좌표로 갱신합니다.
4. **빈 클러스터 예외 처리:** 특정 클러스터에 단 하나의 샘플도 할당되지 않아 비어 있게 되는 경우, 해당 클러스터의 중심점은 기존 좌표를 그대로 유지합니다.

#### 입력

- 첫 번째 줄: 중심 0의 좌표 `c0_x c0_y`가 공백으로 주어집니다.
- 두 번째 줄: 중심 1의 좌표 `c1_x c1_y`가 공백으로 주어집니다.
- 세 번째 줄: 샘플의 수 `N`이 주어집니다.
- 네 번째 줄부터 `N`개 줄: 각 샘플의 좌표 `x y`가 공백으로 구분되어 주어집니다.

- `1 ≤ N ≤ 1,000`
- 모든 좌표 값은 유한한 실수입니다.

#### 출력

- 첫 번째 줄: 원본 샘플 순서에 따른 클러스터 할당 번호(`0` 또는 `1`)를 공백으로 구분하여 출력합니다.
- 두 번째 줄: 갱신된 중심 0의 좌표 `new_c0_x new_c0_y`를 소수점 넷째 자리까지 반올림하여 출력합니다.
- 세 번째 줄: 갱신된 중심 1의 좌표 `new_c1_x new_c1_y`를 소수점 넷째 자리까지 반올림하여 출력합니다.

**예제 입력**

```text
0 0
6 0
3
1 0
5 0
3 0
```

**예제 출력**

```text
ASSIGNMENTS 0 1 0
CENTER_0 2.0000 0.0000
CENTER_1 5.0000 0.0000
```

#### 검증 항목 (Edge Cases)

- **동점 거리 처리:** 두 중심점까지의 거리가 정확히 동일한 샘플이 입력되었을 때, 우선순위 규칙에 따라 안정적으로 처리되는지 확인
- **빈 클러스터(Empty Cluster) 방어:** 데이터 분포에 의해 어느 한쪽 클러스터에 샘플이 단 하나도 할당되지 않는 상황 처리
- **단일 샘플 입력:** `N = 1`인 최소 조건에서도 할당 및 갱신 로직이 정상 작동하는지 확인
- **단발성 갱신 보장:** 중심 갱신을 반복 수행하지 않고, 최초 할당 결과를 바탕으로 **정확히 한 번만** 수행하는지 엄격히 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **제곱 거리 활용:** 유클리드 거리를 비교할 때 제곱근 연산을 생략하고 거리의 제곱(`(x - cx)**2 + (y - cy)**2`) 값을 비교하여 연산 효율성과 정밀도를 높이세요.
2. **동기화 및 순서 분리:** 모든 샘플에 대한 클러스터 할당을 완전히 끝마친 뒤에 중심점 갱신 연산을 수행하세요.
3. **갱신 시점 주의:** 갱신된 새로운 중심 좌표를 이미 할당이 진행 중인 다른 샘플 판정에 즉시 반영하지 않도록 독립적인 단계를 유지하세요.

</details>

---

## Advanced

### A-01. Visitor Congestion Classification — 혼잡도 판단 및 최적 임계값 탐색

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Logistic Regression · Decision Threshold · [Chapter 04](../Chapter-04/README.md) · Confusion Matrix · Precision · Recall · F1-Score · Model Evaluation

#### 문제 설명

지역 문화시설은 방문객 수와 근무 인원 등의 데이터를 활용하여 특정 시간대의 혼잡 여부를 예측하는 분류 모델을 운영하고 있습니다. 운영팀의 정책에 따라 혼잡 상황을 놓치지 않는 것(Recall 중시)과 불필요한 오경보를 줄이는 것(Precision 중시) 사이의 균형을 맞추는 것이 중요합니다.

본 과제에서는 모델이 출력한 클래스 1(혼잡)에 대한 예측 점수(`score`)를 바탕으로, 검증 데이터(Validation Data)를 통해 최적의 결정 임계값(Threshold)을 탐색하고, 확정된 임계값을 독립적인 테스트 데이터(Test Data)에 적용하여 최종 성능을 평가 및 리포팅하는 프로그램을 작성하시오.

#### 요구 사항

1. **데이터 로드:** `record_id`, 실제 레이블(`actual`, `0` 또는 `1`), 예측 점수(`score`, `0 이상 1 이하`)가 포함된 검증용 및 테스트용 CSV 파일을 읽어 들입니다.
2. **검증 데이터 평가:** 임계값 후보군인 `[0.30, 0.50, 0.70]` 각각에 대해 검증 데이터셋에서의 $F_1$-Score를 계산합니다.
3. **최적 임계값 선정:** $F_1$-Score가 가장 높은 임계값을 선택합니다. 만약 동일한 최고 $F_1$-Score를 기록하는 후보가 여러 개인 경우, **더 큰 임계값**을 우선적으로 선택합니다.
4. **테스트 평가:** 선정된 최적의 임계값으로 테스트 데이터셋을 단 한 번 평가하여 혼동 행렬 지표(`TP, FP, FN, TN`)와 성능 지표(`Precision, Recall, F1-Score`)를 기록합니다.
5. **결과 리포트 출력:** 
   - `threshold_report.csv`: 임계값 후보별 검증 $F_1$-Score와 최적선택 여부(`True`/`False`) 기록
   - `test_report.txt`: 최종 선택된 Threshold 및 Test 데이터에 대한 혼동 행렬 및 주요 성능 지표 기록

#### 입력 파일 규격 및 무결성 검증

- **데이터 파일:**
  - `validation_scores.csv`: `record_id,actual,score`
  - `test_scores.csv`: 동일한 열 구조 (실제 레이블 `actual ∈ {0, 1}`, 예측 점수 `0 ≤ score ≤ 1`)
- **공통 제약 조건:** 두 파일 모두 **UTF-8 인코딩**, **헤더 존재**, 그리고 `record_id`의 **중복 불가** 조건(`unique`)을 엄격히 만족해야 합니다.

> ⚠️ **오류 처리 정책:** 누락된 열, 허용 범위를 벗어난 유효하지 않은 값, 또는 중복된 `record_id`가 단 하나라도 발견될 경우, 즉시 해당 파일의 이름과 구체적인 오류 원인을 출력하고 평가 프로세스를 안전하게 중단(Abort)합니다.

#### 출력 파일 규격

총 2개의 결과 파일을 생성하며, 모든 수치 데이터는 **소수점 넷째 자리**까지 반올림하여 기록합니다.

1. **`threshold_report.csv`**
   - 임계값(Threshold) 후보군을 **오름차순**으로 정렬하여 각 후보별 검증 $F_1$-Score와 최적 선택 여부(`True`/`False`)를 기록합니다.
2. **`test_report.txt`**
   - 최종 선정된 최적 Threshold 값과, 해당 Threshold를 테스트 데이터에 적용하여 산출한 혼동 행렬 지표(`TP, FP, FN, TN`) 및 주요 성능 지표를 기록합니다.

**예제 입력** (`validation_scores.csv`)

```csv
record_id,actual,score
R01,0,0.20
R02,1,0.65
R03,1,0.48
R04,0,0.70
```

**예제 출력** (`threshold_report.csv`)

```csv
threshold,validation_f1,selected
0.30,0.8000,1
0.50,0.5000,0
0.70,0.0000,0
```

해당 예제에서 선택된 Threshold는 `0.30`입니다. Test 결과는 별도의 `test_scores.csv` 값에 따라 달라지므로 특정 F1을 고정하지 않습니다.

#### 검증 항목 (Edge Cases)

- **경계값 일치 (`Score == Threshold`):** 예측 점수가 임계값과 정확히 일치하는 샘플들이 올바르게 양성(`1`) 클래스로 분류되는지 확인
- **$F_1$-Score 동점 처리:** 동일한 최고 $F_1$-Score를 기록하는 임계값 후보가 여러 개 존재할 때, **더 큰 값**의 임계값이 우선 선택되는지 엄격히 검증
- **데이터 유출(Data Leakage) 방지:** Validation 단계에서 탐색·확정된 최적 Threshold가 Test 단계에서 변경되거나 재적용되지 않고 독립적으로 유지되는지 확인
- **극한 데이터 및 무결성 예외:** 실제 레이블(`actual`)이 단 하나의 클래스로만 구성된 극단적 상황이나, 잘못된 형식·범위의 CSV 값이 입력되었을 때 프로그램이 안전하게 에러를 처리하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 지표 연산 모듈화 (Modularize Metrics):** 
   - 특정 Threshold를 기준으로 예측 레이블을 생성(`score >= threshold`)하고, `TP`, `FP`, `FN`, `TN`을 집계하여 $F_1$-Score를 반환하는 공용 함수를 정의합니다.
   - Validation과 Test 단계 모두 이 단일 함수를 호출하여 평가 로직의 중복을 막고 일관성을 유지합니다.
   - 참고용 코드 조각(Code Snippet):
     ```python
     def evaluate_metrics(actuals, scores, threshold):
       preds = (scores >= threshold).astype(int)
       tp = ((actuals == 1) & (preds == 1)).sum()
       fp = ((actuals == 0) & (preds == 1)).sum()
       fn = ((actuals == 1) & (preds == 0)).sum()
       tn = ((actuals == 0) & (preds == 0)).sum()

       denom = 2 * tp + fp + fn
       f1 = (2 * tp / denom) if denom > 0 else 0.0
       return tp, fp, fn, tn, f1
     ```

**STEP 2. 최적 Threshold 탐색 및 동점 처리 (Selection & Tie-breaking):**
   - 후보군 `[0.30, 0.50, 0.70]`을 **오름차순**으로 순회하며 검증 $F_1$-Score를 계산합니다.
   - 최고 $F_1$-Score를 갱신할 때 엄격한 대소 비교(`>`)를 사용하되, **동점인 경우 더 큰 임계값**이 선택되도록 조건식(`f1 >= best_f1`)을 설계합니다.
   - 참고용 코드 조각(Code Snippet):
     ```python
     candidates = [0.30, 0.50, 0.70]
     best_threshold = -1.0
     best_f1 = -1.0

     for th in sorted(candidates):
       _, _, _, _, val_f1 = evaluate_metrics(val_actual, val_score, th)
       # 동점 시 더 큰 값을 선택하기 위해 '>=' 적용
       if val_f1 >= best_f1:
         best_f1 = val_f1
         best_threshold = th
     ```

**STEP 3. 데이터 유출 방지 및 독립 평가 파이프라인 (Independent Evaluation):**
   - Validation 데이터로 최종 확정된 `best_threshold`는 상수로 고정합니다.
   - Test 데이터셋 평가 시에는 탐색 과정을 거치지 않고, 확정된 `best_threshold`를 바로 적용하여 단 한 번의 평가(`evaluate_metrics` 호출)만 수행한 뒤 지정된 형식으로 리포트를 출력합니다.

</details>

---

### A-02. Water Consumption Prediction — 수도 사용량 예측 및 성능 비교

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Linear Regression · Feature Scaling · [Chapter 04](../Chapter-04/README.md) · Baseline · MAE · RMSE · Residual · Temporal Split

#### 문제 설명

건물 관리팀은 기온, 건물 이용 인원, 주말 여부 등의 환경 및 운영 데이터를 활용하여 다음 날의 수도 사용량(`consumption_m3`)을 예측하는 회귀 모델을 운영하고자 합니다. 수도 사용량 데이터는 시간의 흐름에 따른 트렌드가 존재하므로, 무작위 행 분할(Random Split)이 아닌 시간 순서를 고려한 분할 방식을 적용해야 합니다.

본 과제에서는 시계열 특성을 반영하여 데이터를 분할한 뒤, 훈련 데이터로 Ridge 회귀 모델을 학습시키고, 하이퍼파라미터 튜닝을 거쳐 단순 평균 예측(Baseline) 모델과 성능을 비교·평가하는 프로그램을 작성하시오.

#### 요구 사항

1. **시계열 데이터 분할 (Temporal Split):** 
   - 데이터를 날짜(`date`) 기준 오름차순으로 정렬합니다.
   - 전체 샘플 수 `N`을 기준으로 과거 `60%`를 Train, 이후 `20%`를 Validation, 마지막 `20%`를 Test 데이터로 분할합니다.
   - 데이터 수가 정확히 나누어떨어지지 않는 경우, Train과 Validation은 각각 `floor(0.6 * N)`, `floor(0.2 * N)` 개로 설정하고 남은 잔여 샘플은 모두 Test에 배정합니다.
2. **특징(Feature) 및 타겟(Target) 정의:**
   - 예측 모델의 입력(Feature)으로 `temperature_c`, `occupants`, `is_weekend` 세 개의 열을 사용하고, 타겟(Target)으로 `consumption_m3`를 지정합니다. `date` 자체는 피처에서 제외합니다.
3. **베이스라인 및 모델 파이프라인 구축:**
   - 훈련 데이터 타겟의 평균값을 예측값으로 사용하는 단순 베이스라인(Baseline) 모델을 정의합니다.
   - 수치형 피처의 정규화를 위한 `StandardScaler`와 선형 회귀 모델인 `Ridge`를 결합한 파이프라인을 구축합니다.
4. **하이퍼파라미터 튜닝 (Validation 평가):**
   - Ridge 모델의 규제 계수 `alpha` 후보군인 `[0.1, 1.0, 10.0]` 각각에 대해 Validation 데이터셋의 MAE(Mean Absolute Error)를 측정하여 최적의 값을 탐색합니다.
   - 만약 동일한 최고 성능을 기록하는 `alpha` 후보가 여러 개인 경우, **더 작은 `alpha`**를 우선적으로 선택합니다.
5. **테스트 평가 및 결과 리포트 생성:**
   - 확정된 최적의 모델 설정을 바탕으로 Test 데이터셋에 대한 최종 성능 지표(MAE, RMSE)를 산출합니다.
   - 평가 결과로서 `date`, 실제값(`actual`), 예측값(`predicted`), 그리고 잔차(`residual = actual - predicted`)를 포함하는 결과 CSV 파일을 생성합니다.

#### 입력

- **데이터 파일:** `daily_water.csv` (`date,temperature_c,occupants,is_weekend,consumption_m3`)
- **데이터 제약 조건:**
  - 날짜(`date`)는 `YYYY-MM-DD` 형식이며 중복되지 않습니다.
  - `is_weekend`는 `0` 또는 `1`, `occupants`는 `0` 이상의 정수입니다.
  - 모든 수치 값(기온, 수도 사용량 등)은 유한한 실수 또는 정수여야 합니다.
  - 평가는 최소 30개 행 이상의 데이터셋을 대상으로 수행합니다.

**예제 입력 일부**

```csv
date,temperature_c,occupants,is_weekend,consumption_m3
2026-04-01,17.0,42,0,48.5
2026-04-02,19.0,44,0,52.1
2026-04-03,21.0,36,0,49.3
```

#### 출력

프로그램 실행 결과로 총 3개의 파일이 생성되어야 하며, 모든 수치 지표는 소수점 넷째 자리까지 반올림하여 기록합니다.

1. **`model_comparison.csv` (`model,validation_mae`)**
   - 단순 평균 예측(Baseline) 모델과 Ridge 하이퍼파라미터 `alpha` 후보군별(예: `alpha=0.1, 1.0, 10.0`) Validation MAE 성능 결과를 기록합니다.
2. **`test_predictions.csv` (`date,actual,predicted,residual`)**
   - Test 데이터셋에 속한 각 날짜(`date`)별 실제값(`actual`), 예측값(`predicted`), 그리고 잔차(`residual = actual - predicted`)를 기록합니다. (Test 날짜 기준 **오름차순 정렬**)
3. **`report.txt`**
   - 최종 선택된 `alpha` 값, Test 데이터셋에 대한 모델의 MAE·RMSE, Baseline MAE, 그리고 모델과 Baseline 간의 성능 비교 결과를 텍스트 형식으로 요약하여 기록합니다.

**(※ 참고: 채점 및 평가는 최소 30행 이상의 전체 데이터셋을 대상으로 수행되며, 예제 입력 데이터만으로 학습 및 평가가 진행되지 않습니다.)**

#### 검증 항목 (Edge Cases & Validation Rules)

- **시계열 분할 무결성 (Temporal Split Integrity):** 날짜(`date`) 기준 오름차순 정렬 후 Train(60%), Validation(20%), Test(20%) 세 구간으로 순서에 맞게 엄격히 분할되었으며, 구간 간 데이터의 누락이나 중복(Overlap)이 발생하지 않는지 확인
- **데이터 유출 방지 (No Data Leakage):** 특징 스케일링(`StandardScaler`) 및 모델 학습 시 Validation과 Test 데이터셋의 정보(타겟 통계량 등)가 일절 참조되거나 학습에 영향을 주지 않는지 확인 (특히 스케일러는 Train 데이터를 기준으로만 `fit` 되어야 함)
- **독립적 하이퍼파라미터 선정 (Independent Model Selection):** Validation 데이터셋을 통해 탐색·확정된 최적의 `alpha` 값이 Test 데이터셋의 성능에 의해 변경되거나 재선택되지 않고 독립적으로 고정되는지 확인
- **잔차 및 지표 산출 정합성 (Residual & Metrics Verification):** 
  - 잔차(`residual`)가 명세된 공식(`actual - predicted`)과 정확한 부호 및 값으로 계산되는지 검증
  - `test_predictions.csv` 내 레코드가 Test 날짜 기준 오름차순으로 올바르게 정렬되어 있는지 확인
  - MAE 및 RMSE 지표가 수식에 맞게 오차 없이 산출되었는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 시계열 데이터 로드 및 Temporal Split 분할**
   - 데이터를 읽어 들인 후 날짜(`date`) 컬럼을 기준으로 오름차순 정렬합니다.
   - 전체 행 수 `N`을 기준으로 Train(60%), Validation(20%), Test(20%) 구간으로 분할합니다. 정확히 나누어떨어지지 않을 경우, `floor(0.6 * N)`과 `floor(0.2 * N)` 공식을 적용하고 잔여 샘플은 Test에 배정합니다.
     ```python
     # 힌트: 날짜 정렬 및 위치 기반 분할 예시
     import pandas as pd

     df = pd.read_csv("daily_water.csv")
     df["date"] = pd.to_datetime(df["date"])
     df = df.sort_values("date").reset_index(drop=True)

     n = len(df)
     train_end = int(n * 0.6)
     val_end = train_end + int(n * 0.2)

     train_df = df.iloc[:train_end]
     val_df = df.iloc[train_end:val_end]
     test_df = df.iloc[val_end:]

**STEP 2. 파이프라인 구축 및 Baseline 설정**
   - 사이킷런의 `Pipeline`을 활용하여 `StandardScaler`와 `Ridge` 회귀 모델을 하나로 묶습니다.
   - Baseline 모델은 훈련 데이터 타겟(`consumption_m3`)의 평균값으로 고정하여 예측 오차(MAE)의 기준점으로 삼습니다.
     ```python
     from sklearn.linear_model import Ridge
     from sklearn.pipeline import Pipeline
     from sklearn.preprocessing import StandardScaler
   
     # 피처 및 타겟 정의
     features = ["temperature_c", "occupants", "is_weekend"]
     target = "consumption_m3"
   
     # Baseline 예측값 (Train Target의 평균)
     baseline_pred = train_df[target].mean()
     ```

**STEP 3. 하이퍼파라미터 탐색 및 최적 `alpha` 선정 (동점 처리 고려)**
   - `alpha` 후보군(`[0.1, 1.0, 10.0]`)을 순회하며 파이프라인을 훈련 데이터로 학습시키고, Validation 데이터에 대한 MAE를 측정합니다.
   - 성능이 동점일 경우 **더 작은 `alpha`**를 우선 선택하도록 조건식을 구성하고, 모델 결정을 완료합니다.
     ```python
     from sklearn.metrics import mean_absolute_error
   
     alphas = [0.1, 1.0, 10.0]
     best_alpha = None
     best_mae = float("inf")
   
     for alpha in alphas:
       pipe = Pipeline([
           ("scaler", StandardScaler()),
           ("model", Ridge(alpha=alpha)),
       ])
       pipe.fit(train_df[features], train_df[target])
       val_preds = pipe.predict(val_df[features])
   
       # Validation MAE 계산
       val_mae = mean_absolute_error(val_df[target], val_preds)
   
       # 동점 시 더 작은 alpha 선택을 위해 '<' 적용 (오름차순 순회 시 첫 번째로 작은 값이 유지됨)
       if val_mae < best_mae:
         best_mae = val_mae
         best_alpha = alpha
     ```

**STEP 4. 최종 모델 평가 및 결과 리포트 파일 생성**
   - 탐색을 통해 확정된 최적의 `alpha`로 최종 파이프라인을 학습시키고, Test 데이터셋에 대한 예측 및 성능 지표(MAE, RMSE)를 산출합니다.
   - 잔차(`residual = actual - predicted`)를 계산하고, 요구되는 3개의 파일(`model_comparison.csv`, `test_predictions.csv`, `report.txt`)로 결과물을 각각 저장합니다.
     ```python
     import numpy as np
     from sklearn.metrics import mean_absolute_error
   
     # 최적 alpha로 최종 모델 학습
     final_pipe = Pipeline([
         ("scaler", StandardScaler()),
         ("model", Ridge(alpha=best_alpha)),
     ])
     final_pipe.fit(train_df[features], train_df[target])
   
     # Test 예측 및 지표 계산
     test_preds = final_pipe.predict(test_df[features])
     test_actuals = test_df[target].values
   
     test_mae = mean_absolute_error(test_actuals, test_preds)
     test_rmse = np.sqrt(np.mean((test_actuals - test_preds) ** 2))
   
     # Test Baseline MAE 계산
     baseline_test_preds = np.full_like(test_actuals, baseline_pred)
     baseline_test_mae = mean_absolute_error(test_actuals, baseline_test_preds)
   
     # 잔차 계산 및 test_predictions.csv 저장 (날짜 오름차순)
     test_result_df = test_df[["date"]].copy()
     test_result_df["actual"] = test_actuals
     test_result_df["predicted"] = test_preds
     test_result_df["residual"] = test_actuals - test_preds
     test_result_df.to_csv("test_predictions.csv", index=False)
     ```
     
</details>

---

### A-03. Unlabeled Usage Pattern Analysis — 비지도 학습 기반 이용 패턴 군집화

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · DBSCAN · Feature Scaling · Cluster Profile · Noise Handling

#### 문제 설명

공유 공간의 방문 기록 데이터에는 사용자의 유형을 사전에 정의하는 정답 레이블(Label)이 존재하지 않습니다. 운영팀은 방문 빈도(`weekly_visits`), 체류 시간(`avg_minutes`), 저녁 이용 비율(`evening_ratio`) 등의 지표를 활용하여 숨겨진 사용자 이용 패턴을 발견하고자 합니다.

본 과제에서는 비지도 학습 알고리즘인 KMeans와 DBSCAN을 각각 적용하여 데이터를 군집화하고, 두 알고리즘의 특성 차이를 이해하며, 각 군집의 통계적 프로파일을 분석하여 공간 운영 전략 수립을 위한 보고서를 작성하는 프로그램을 구현하시오.

#### 요구 사항

1. **데이터 무결성 검증 및 전처리:**
   - `weekly_visits`, `avg_minutes`, `evening_ratio` 피처의 결측값 및 유효하지 않은 범위(예: 음수 값, 비율의 허용 범위를 벗어난 값 등)를 엄격히 검사합니다.
   - 규칙을 위반한 비정상 행(Invalid rows)은 별도의 `invalid_rows.csv` 파일로 저장하고, 이후 군집화 분석 대상에서 제외합니다.
2. **특징 스케일링 (Feature Scaling):**
   - 정제된 유효 데이터의 피처들에 `StandardScaler`를 적용하여 각 변수의 스케일을 정규화합니다.
3. **군집화 모델 실행:**
   - `KMeans(n_clusters=3, random_state=42, n_init=10)` 모델을 실행하여 지정된 수의 군집으로 할당합니다.
   - `DBSCAN(eps=0.6, min_samples=5)` 모델을 실행하여 밀도 기반 군집화를 수행합니다.
4. **군집 프로파일링 및 통계 집계:**
   - 두 모델 각각에 대해 각 군집의 크기(샘플 수)와 원본 데이터 단위 기준 Feature별 평균값을 계산합니다.
   - 특히 DBSCAN 결과에서 노이즈(Noise)를 나타내는 레이블(`-1`)은 별도의 그룹으로 분리하여 집계합니다.
5. **결과물 출력 및 보고서 작성:**
   - `cluster_assignments.csv`(개별 샘플별 KMeans 및 DBSCAN 군집 할당 결과), `cluster_profiles.csv`(군집별 통계 프로파일), `report.md`(분석 결과 보고서)를 생성합니다.
   - 보고서 작성 시, KMeans와 DBSCAN의 Cluster ID는 알고리즘 구조상 동일한 의미나 대응 관계를 갖지 않음을 명시하고 두 모델의 특성을 비교·설명합니다.

#### 입력

- **데이터 파일:** `space_usage.csv` (`record_id,weekly_visits,avg_minutes,evening_ratio`)
- **데이터 제약 조건:**
  - `record_id`: 고유 식별자 (문자열 또는 정수)
  - `weekly_visits`: `0` 이상의 정수 (주간 방문 횟수)
  - `avg_minutes`: `0` 이상의 유한한 실수 (평균 체류 시간)
  - `evening_ratio`: `0` 이상 `1` 이하의 실수 (저녁 시간대 이용 비율)
  - **최소 샘플 요건:** 무결성 검증을 통과한 유효한 샘플 수는 **최소 30개 이상**이어야 하며, 30개 미만일 경우 예외를 발생시키거나 분석 프로세스를 즉시 중단해야 합니다.

**예제 입력 일부**

```csv
record_id,weekly_visits,avg_minutes,evening_ratio
S01,2,135,0.15
S02,7,32,0.82
S03,3,102,0.38
```

#### 출력 파일 규격

프로그램 실행 결과로 총 4개의 파일이 생성되어야 하며, 모든 수치 지표(평균값 등)는 소수점 넷째 자리까지 반올림하여 기록합니다.

1. **`cluster_assignments.csv` (`record_id,kmeans_cluster,dbscan_cluster`)**
   - 무결성 검증을 통과한 원본 유효 행의 순서(`record_id`)를 유지한 채, 각 샘플이 KMeans와 DBSCAN에서 각각 할당받은 군집 번호(Cluster ID)를 기록합니다. (DBSCAN 노이즈는 `-1`로 표기)
2. **`cluster_profiles.csv` (`method,cluster_id,sample_count,mean_weekly_visits,mean_avg_minutes,mean_evening_ratio`)**
   - 두 알고리즘(`kmeans`, `dbscan`)별 각 군집 및 노이즈 그룹의 샘플 수(`sample_count`)와, 원본 단위 데이터 기준 Feature별 평균 통계량을 요약하여 기록합니다.
3. **`invalid_rows.csv` (`row_number,error_code`)**
   - 무결성 검증 규칙(결측값, 허용 범위를 벗어난 값 등)을 위반한 비정상 행의 원본 파일 내 행 번호와 에러 코드를 기록합니다. (위반 행이 존재하지 않을 경우, 헤더만 출력합니다.)
4. **`report.md`**
   - 각 군집별 이용 패턴의 주요 특징, DBSCAN 알고리즘에서 발생한 노이즈(Noise) 데이터의 수, 그리고 두 알고리즘 간 군집 구조의 차이점 및 해석상 한계를 서술한 마크다운 형식의 보고서를 작성합니다.

*(※ 주의: 군집 번호와 통계 평균값은 전체 데이터셋의 분포에 따라 동적으로 결정되므로, 예제 입력 데이터만으로 결과를 미리 고정하여 하드코딩하지 않도록 주의합니다.)*

#### 검증 항목 (Edge Cases & Validation Rules)

- **비정상 행 완벽 격리 (Exclusion of Invalid Rows):** 무결성 검증 단계에서 포착된 비정상 행(`invalid_rows.csv` 대상)이 피처 스케일링(`StandardScaler`)이나 군집화 모델 학습·할당 과정에 일절 포함되지 않고 안전하게 격리되는지 확인
- **DBSCAN 노이즈 집계 누락 방지 (Noise Handling):** DBSCAN 알고리즘 수행 결과 노이즈로 판별된 샘플(`cluster_id = -1`)이 군집 프로파일링(`cluster_profiles.csv`) 과정에서 누락되지 않고 별도의 그룹으로 정확히 집계되는지 검증
- **샘플 수 무결성 일치 (Sample Count Integrity):** 전체 유효 샘플 수(무결성 검증 통과 데이터 수)와 KMeans 군집별 샘플 수의 총합(`sample_count` 합계)이 정확히 일치하는지 확인
- **비지도 학습 해석의 유의성 (Unsupervised Interpretation Guard):** 도출된 Cluster ID를 사전에 정의된 절대적인 '정답 레이블(Ground Truth)'이나 실제 이용자 유형의 고정된 실체로 오인하지 않고, 각 알고리즘의 구조적 특성에 기반한 상대적 군집으로 올바르게 해석하는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 데이터 무결성 검증 및 비정상 행 격리**
   - `weekly_visits`, `avg_minutes`, `evening_ratio` 피처의 결측값 및 허용 범위 위반 여부를 검사하는 로직을 작성합니다.
   - 규칙을 위반한 행은 `invalid_rows.csv`에 기록하고, 정상 행만 추출하여 유효 샘플 수(최소 30개)를 검증합니다.
     ```python
     import pandas as pd
   
     df = pd.read_csv("space_usage.csv")
     invalid_rows = []
     valid_indices = []
   
     for idx, row in df.iterrows():
       row_num = idx + 2  # CSV 헤더 고려
       # TODO: 결측치 확인 및 유효 범위 조건식 완성
       # (weekly_visits >= 0, avg_minutes >= 0, 0 <= evening_ratio <= 1)
       if False:  # 조건식 수정 필요
         invalid_rows.append({"row_number": row_num, "error_code": "INVALID_VALUE"})
       else:
         valid_indices.append(idx)
   
     invalid_df = pd.DataFrame(invalid_rows)
     invalid_df.to_csv("invalid_rows.csv", index=False)
   
     valid_df = df.iloc[valid_indices].reset_index(drop=True)
     # TODO: 유효 샘플 수가 30개 미만일 경우 예외 발생 또는 분석 중단 로직 작성
     ```

**STEP 2. 특징 스케일링 (Feature Scaling)**
   - Clustering의 거리 계산 왜곡을 방지하기 위해 정제된 유효 데이터로부터 피처를 추출하고 스케일링을 수행합니다.
     ```python
     from sklearn.preprocessing import StandardScaler
   
     features = ["weekly_visits", "avg_minutes", "evening_ratio"]
     
     # TODO: StandardScaler 객체 생성 및 fit_transform을 통한 유효 피처 스케일링 구현
     scaler = None
     scaled_features = None
     ```
**STEP 3. 군집화 모델 실행 및 할당 결과 기록**
   - 지정된 파라미터로 `KMeans`와 `DBSCAN`을 각각 실행하고, 원본 유효 행의 순서와 일치하도록 군집 할당 결과를 수집하여 저장합니다.
     ```python
     from sklearn.cluster import DBSCAN, KMeans
   
     # TODO: KMeans 객체 생성 및 학습·예측 수행 (n_clusters=3, random_state=42, n_init=10)
     kmeans_labels = None
   
     # TODO: DBSCAN 객체 생성 및 학습·예측 수행 (eps=0.6, min_samples=5)
     dbscan_labels = None
   
     # TODO: 원본 유효 행의 record_id와 군집 할당 결과를 포함하는 DataFrame 생성 후 cluster_assignments.csv 저장
     assignments_df = valid_df[["record_id"]].copy()
     # assignments_df["kmeans_cluster"] = ...
     # assignments_df["dbscan_cluster"] = ...
     ```

**STEP 4. 원본 단위 군집 프로파일링 및 리포트 작성**
   - 운영팀이 해석하기 쉽도록 스케일링된 값이 아닌 **원본 데이터 단위(`valid_df`)**에서 군집별 샘플 수와 Feature별 평균값을 계산합니다. (DBSCAN의 노이즈 `-1` 포함)
   - 집계된 프로파일을 `cluster_profiles.csv`로 저장하고, 알고리즘별 특성과 차이를 기술한 `report.md` 작성의 기초 자료로 활용합니다.
     ```python
     import pandas as pd
   
     profiles = []
   
     # TODO: KMeans 각 군집별(노이즈 또는 레이블별) sample_count 및 원본 feature 평균 계산 로직 작성
     # TODO: DBSCAN 각 군집 및 노이즈(-1)별 sample_count 및 원본 feature 평균 계산 로직 작성
   
     # TODO: 결과를 DataFrame으로 변환하고 소수점 넷째 자리 반올림 후 cluster_profiles.csv 저장
     ```
</details>

---

### A-04. Misleading Validation Score — 데이터 유출(Data Leakage) 및 잘못된 평가 흐름 교정

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Data Leakage · [Chapter 04](../Chapter-04/README.md) · Pipeline · Cross-Validation · Hyperparameter Tuning

#### 문제 설명

어느 개발자가 머신러닝 모델의 성능을 극대화하기 위해 K-Nearest Neighbors(KNN) 알고리즘의 이웃 수(`n_neighbors`)를 반복적으로 튜닝하였습니다. 보고서상 교차 검증(Cross-Validation) 점수는 매우 높게 측정되었으나, 실제 구현된 소스 코드를 면밀히 검토한 결과 몇 가지 치명적인 평가 오류가 발견되었습니다.

첫째, 전체 데이터셋을 대상으로 특징 스케일링(`StandardScaler`)을 먼저 수행한 뒤 학습용 데이터와 평가용 데이터로 분할하여 **데이터 유출(Data Leakage)**이 발생했습니다. 둘째, 하이퍼파라미터 탐색 및 최적 모델 선정 과정에서 평가용 데이터셋(Test Set)의 성능을 여러 차례 참조하여 사실상 테스트 데이터가 모델 학습 과정에 오염(Contamination)되었습니다.

본 과제에서는 위 사례와 같은 치명적인 평가 오류의 원인을 분석하고, 사이킷런의 `Pipeline`과 올바른 데이터 분할·교차 검증 원칙을 적용하여 데이터 유출을 방지하는 안전한 평가 파이프라인을 구축하시오.

**문제가 있는 코드**

```python
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
search = GridSearchCV(
    KNeighborsClassifier(), {"n_neighbors": [3, 5, 7]}, cv=5
)
search.fit(X_train, y_train)
# 이후 Test 점수를 반복 확인해 n_neighbors를 변경함
```

#### 구현 요구사항

1. **평가 절차 오류 분석:** 기존 코드에서 발생하는 머신러닝 평가 절차상 및 통계적 오류(데이터 유출 및 테스트 세트 오염 등)를 두 가지 이상 식별하고 구체적으로 설명합니다.
2. **데이터 분할 우선 원칙 준수:** 원본 데이터(`X`, `y`)를 모델 학습 및 전처리 이전에 `train_test_split`을 통해 훈련 세트와 테스트 세트로 선분할합니다. (단, 본 문제는 독립 샘플로 구성된 이진 분류 데이터셋이며 클래스별 샘플이 충분하다고 가정)
3. **파이프라인 및 교차 검증 적용:** `StandardScaler`와 `KNeighborsClassifier`를 `Pipeline`으로 결합하고, `GridSearchCV`를 활용하여 교차 검증(`CV`) 폴드 내에서 전처리가 독립적으로 수행되도록 구성하여 `n_neighbors` 후보를 탐색합니다.
4. **최종 테스트 평가 단회성 보장:** 하이퍼파라미터 튜닝 및 모델 선택 과정에서 테스트 세트를 일절 참조하지 않고 완전히 격리한 뒤, 최적화가 완료된 최종 모델에 대해 독립된 테스트 데이터에서 정확도(`Accuracy`)와 균형 정확도(`Balanced Accuracy`)를 **단 한 번만** 평가합니다.
5. **감사 보고서 작성 (`audit_report.md`):** 기존 코드의 구조적 문제점, 수정된 파이프라인의 처리 순서 및 데이터 흐름, 그리고 평가 과정에서 각 데이터셋(Train/Validation/Test)이 수행하는 역할과 통제 방안을 마크다운 보고서로 서술합니다.

#### 입력 데이터 규격 및 제약 사항

- **입력 변수:**
  - `X`: Shape `(N, D)`인 실수형 독립 변수(Feature) 배열
  - `y`: Shape `(N,)`인 이진 분류 타겟(Target) 배열 (`0` 또는 `1`)
- **데이터 규격 조건:**
  - 샘플 수 $N \ge 100$, 피처 차원 $D \ge 2$
  - 각 클래스별 샘플 수는 5-Fold 교차 검증(`cv=5`)을 안정적으로 수행하기에 충분한 수량을 확보하고 있습니다.
- **실습/테스트 데이터 생성 안내:**
  - 독립된 가상 검증용 데이터셋이 필요한 경우, 아래의 사이킷런 유틸리티 함수를 활용하여 생성할 수 있습니다.
    ```python
    from sklearn.datasets import make_classification

    X, y = make_classification(
        n_samples=400,
        n_features=5,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    ```

#### 출력 파일 규격

프로그램 실행 결과로 총 3개의 파일이 생성되어야 하며, 모든 성능 수치 및 지표는 소수점 넷째 자리까지 반올림하여 기록합니다.

1. **`best_params.json`**
   - 하이퍼파라미터 튜닝을 통해 최적으로 선정된 `n_neighbors` 값과 해당 모델의 평균 교차 검증 정확도(`mean_cv_accuracy`)를 기록합니다.
   - **JSON 예시 구조:**
     ```json
     {
       "best_n_neighbors": 5,
       "mean_cv_accuracy": 0.8525
     }
     ```
2. **`test_metrics.json`**
   - 완전히 격리된 테스트 세트를 활용하여 단 한 번 평가한 최종 성능 지표인 정확도(`test_accuracy`)와 균형 정확도(`test_balanced_accuracy`)를 기록합니다.
   - **JSON 예시 구조:**
     ```json
     {
       "test_accuracy": 0.8625,
       "test_balanced_accuracy": 0.8600
     }
     ```
3. **`audit_report.md`**
   - 기존 코드에서 발생한 구조적 평가 오류(전체 데이터 스케일링으로 인한 데이터 유출, 테스트 세트 반복 참조 등), 이를 바로잡기 위한 `Pipeline` 도입 및 데이터 분할 순서 수정 이유, 그리고 평가 과정에서 각 데이터셋(Train/Test)이 수행한 역할에 대한 검증 보고서를 마크다운 형식으로 작성합니다.

*(※ 주의: 본 과제는 특정 고정 성능 목표치의 달성 여부를 채점하는 것이 아니라, **데이터 유출을 원천 차단하고 평가 단계를 엄격하게 분리한 올바른 머신러닝 평가 파이프라인 흐름**을 구현했는지를 중점적으로 검증합니다.)*

#### 검증 항목 (Edge Cases & Validation Rules)

- **데이터 유출 차단 검증:** `StandardScaler.fit()` 등의 전처리기 학습이 테스트 세트(Test Data)나 교차 검증 각 폴드(CV Fold)의 검증 데이터 영역을 일절 참조하거나 오염시키지 않고, 오직 훈련 데이터 내부에서만 독립적으로 수행되는지 확인
- **테스트 데이터 격리 원칙:** 하이퍼파라미터 튜닝 및 모델 선택 과정에서 테스트 세트의 평가 결과를 피드백 루프로 사용하여 후보 모델을 재선택하거나 수정하는 부적절한 탐색 행위가 원천 차단되었는지 확인
- **파이프라인 파라미터 매핑 정합성:** `GridSearchCV`의 `param_grid` 설정 시 `Pipeline` 내에 정의된 컴포넌트 명칭과 파라미터가 올바르게 연결(예: 네이밍 규격에 맞는 `n_neighbors` 탐색 설정)되어 정상적으로 작동하는지 검증
- **재현성 확보:** 데이터 분할(`train_test_split`) 및 모델 학습 과정에서 무작위성이 개입되는 모든 단계에 동일한 `random_state`가 적용되어 일관된 데이터 분할과 재현 가능한 결과가 보장되는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 데이터 분할 우선 수행 (Data Leakage 방지)**
   - 모델 학습 및 전처리(스케일링 등)를 수행하기 전에, 전체 원본 데이터 `X`와 `y`를 `train_test_split()`을 통해 훈련 세트와 테스트 세트로 먼저 분할합니다.
     ```python
     from sklearn.model_selection import train_test_split
   
     # TODO: X와 y를 train_test_split으로 분할 (test_size=0.2, random_state=42, stratify=y)
     X_train, X_test, y_train, y_test = None, None, None, None
     ```
**STEP 2. Pipeline 구성 및 GridSearchCV 설정**
   - `StandardScaler`와 `KNeighborsClassifier`를 `Pipeline`으로 결합하고, 교차 검증 폴드 내부에서 전처리가 독립적으로 수행되도록 합니다.
   - `GridSearchCV`를 통해 탐색할 하이퍼파라미터 그리드를 설정합니다. (예: `model__n_neighbors`)
     ```python
     from sklearn.model_selection import GridSearchCV
     from sklearn.neighbors import KNeighborsClassifier
     from sklearn.pipeline import Pipeline
     from sklearn.preprocessing import StandardScaler
   
     # TODO: StandardScaler와 KNeighborsClassifier를 포함하는 Pipeline 구성 (예: 단계명 'model' 사용)
     pipeline = Pipeline([("scaler", StandardScaler()), ("model", None)])
   
     # TODO: param_grid 설정 (예: {"model__n_neighbors": [3, 5, 7]})
     param_grid = {}
   
     # TODO: GridSearchCV 객체 생성 (estimator=pipeline, param_grid=param_grid, cv=5)
     search = None
     ```

**STEP 3. 훈련 데이터 기반 하이퍼파라미터 튜닝 및 최적 파라미터 저장**
   - 훈련 데이터(`X_train`, `y_train`)를 대상으로 `GridSearchCV`를 학습시켜 최적의 하이퍼파라미터를 탐색합니다.
   - 탐색된 최적의 `n_neighbors` 값과 최고 교차 검증 평균 정확도를 추출하여 `best_params.json`으로 저장합니다.
     ```python
     import json
   
     # TODO: search.fit(X_train, y_train)을 통한 하이퍼파라미터 튜닝 수행
   
     # TODO: search.best_params_와 search.best_score_를 가져와 딕셔너리 구성 및 best_params.json 저장
     best_params = {
         "best_n_neighbors": None,  # 최적 n_neighbors 값 추출
         "mean_cv_accuracy": None,  # 최고 교차 검증 정확도 (소수점 넷째 자리 반올림)
     }
   
     with open("best_params.json", "w", encoding="utf-8") as f:
       json.dump(best_params, f, ensure_ascii=False, indent=4)
     ```
##### STEP 4. 최종 테스트 평가 수행 및 감사 보고서 작성
   - 튜닝 과정에서 완전히 격리했던 테스트 세트(`X_test`, `y_test`)를 대상으로 최종 모델(`search.best_estimator_`)의 성능을 단 한 번 평가합니다.
   - 정확도(`accuracy_score`)와 균형 정확도(`balanced_accuracy_score`)를 계산하여 `test_metrics.json`으로 저장하고, 기존 코드의 문제점과 개선 내역을 담은 `audit_report.md`를 작성합니다.
     ```python
     import json
     from sklearn.metrics import accuracy_score, balanced_accuracy_score
   
     # TODO: search.best_estimator_를 사용하여 X_test 예측 수행
     y_pred = None
   
     # TODO: accuracy_score 및 balanced_accuracy_score 계산 (소수점 넷째 자리 반올림)
     test_accuracy = None
     test_balanced_accuracy = None
   
     test_metrics = {
         "test_accuracy": test_accuracy,
         "test_balanced_accuracy": test_balanced_accuracy,
     }
   
     with open("test_metrics.json", "w", encoding="utf-8") as f:
       json.dump(test_metrics, f, ensure_ascii=False, indent=4)
   
     # TODO: 기존 코드의 문제점(Data Leakage, Test 세트 오염), Pipeline 도입 이유, 데이터 역할을 기술한 audit_report.md 작성
     report_content = """# 머신러닝 평가 흐름 감사 보고서 (Audit Report)
   
      ## 1. 기존 코드의 평가 절차상 문제점
      - ...
      
      ## 2. 수정된 파이프라인 및 데이터 유출 방지 대책
      - ...
      
      ## 3. 데이터셋별 역할 분담
      - **Train Set**: ...
      - **Validation Set (CV)**: ...
      - **Test Set**: ...
      """
   
     with open("audit_report.md", "w", encoding="utf-8") as f:
       f.write(report_content)
     ```
  
</details>

---

## Professional

### P-01. Warranty Repair Triage — 데이터 유출 방지와 그룹 분할을 적용한 보증수리 우선순위 모델링

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · Human Review · [Chapter 03](../Chapter-03/README.md) · Logistic Regression · [Chapter 04](../Chapter-04/README.md) · Imbalanced Evaluation · F2 · Group-Aware Split · Threshold

#### 문제 설명

가전제품 수리센터에는 매일 수많은 보증수리 접수가 유입되지만, 한정된 인력으로 인해 **하루 최대 3건**의 접수만 우선 검토할 수 있습니다. 접수 건 중 상당수는 단순 사용 미숙이나 안내만으로 해결되는 반면, 실제 하드웨어 고장 판정으로 이어지는 고부가가치 케이스는 제한적입니다. 센터는 실제 고장 확률이 높은 접수를 정확히 선별하여 운영 효율성을 극대화하고자 합니다.

그러나 제공된 히스토리 데이터에는 머신러닝 실무에서 흔히 범하는 치명적인 구조적 오류가 내포되어 있습니다. 
첫째, 동일 제품에 대한 반복 신청 이력이 포함되어 있어 일반적인 무작위 분할(Random Split) 시 학습 데이터와 테스트 데이터 간의 **그룹 유출(Group Leakage)**이 발생합니다. 
둘째, 현장 점검 이후에만 확정되는 '실제 고장 판정 결과'와 '최종 수리 비용' 등의 **후행 지표(Post-Inspection Features)**가 접수 시점의 예측 Feature에 혼입되어 심각한 **데이터 유출(Data Leakage)**을 유발하고 있습니다.

본 과제에서는 그룹 구조를 고려한 데이터 분할 전략을 수립하고, 사후 정보 유출을 원천 차단한 예측 모델을 구축한 뒤, 제한된 운영 자원(일일 최대 3건 검토)과 클래스 불균형을 고려한 최적의 판정 임계값(Threshold) 및 평가 체계를 설계하시오.

#### 제공 데이터

분석 및 운영을 위해 두 개의 데이터셋 파일(`historical_claims.csv`, `incoming_claims.csv`)이 제공되며, 모두 UTF-8 인코딩의 CSV 형식입니다.

1. **`historical_claims.csv` (학습 및 검증용 히스토리 데이터)**
   - 모델 학습, 교차 검증 및 성능 평가에 사용되는 과거 수리 접수 이력 데이터입니다.
   
| 열 이름 | 의미 | 데이터 사용 가이드 / 제약 사항 |
| :--- | :--- | :--- |
| `claim_id` | 접수 번호 | 각 접수를 식별하는 고유 식별자 |
| `received_date` | 접수일 | 데이터 분할 기준 및 시계열 흐름 파악용 |
| `unit_id` | 제품 고유 번호 | **그룹 분할(Group-Aware Split) 기준** (동일 제품의 반복 신청 격리) |
| `age_months` | 제품 사용 개월 수 | 예측 모델의 입력 특징(`Feature`)으로 사용 가능 |
| `alarm_count_30d` | 최근 30일 오류 알림 횟수 | 예측 모델의 입력 특징(`Feature`)으로 사용 가능 |
| `prior_claim_count` | 해당 접수 이전의 누적 수리 신청 수 | 예측 모델의 입력 특징(`Feature`)으로 사용 가능 |
| `confirmed_failure` | 점검 후 실제 고장 여부 (0 또는 1) | 모델 학습 및 평가를 위한 **타겟(Target) 전용** |
| `final_repair_cost` | 점검 후 확정된 수리비 | **사용 금지 (사후 정보 유출 방지를 위해 Feature 및 Target으로 일절 활용 불가)** |

2. **`incoming_claims.csv` (운영 예측 대상 데이터)**
   - 실제 운영 환경에서 타겟 변수(`confirmed_failure`)와 사후 정보(`final_repair_cost`)가 배제된 채 유입되는 신규 접수 데이터입니다.
   - 구성 컬럼: `claim_id, received_date, unit_id, age_months, alarm_count_30d, prior_claim_count`

> ⚠️ **주의 사항:** `unit_id`가 동일한 샘플들은 동일 기기에서 발생한 연쇄 기록이므로, 무작위 분할 시 데이터 유출을 유발합니다. 반드시 그룹 구조를 반영한 분할 방식을 적용해야 합니다.

#### 요구사항

1. **데이터 정합성 검증 및 전처리:** 필수 Feature 누락 여부 및 값의 범위 오류를 검사합니다 (`age_months`, `alarm_count_30d`, `prior_claim_count`는 모두 0 이상의 정수). 유효하지 않은 레코드는 별도로 분리하고 명확한 오류 사유를 기록합니다.
2. **그룹 인식 데이터 분할 (Group-Aware Split):** 제품 단위(`unit_id`)를 기준으로 Train 60%·Validation 20%·Test 20% 비율에 가깝게 분할합니다. 동일한 제품이 서로 다른 세 구간에 중복으로 포함되어서는 안 됩니다 (`GroupShuffleSplit(random_state=42)` 등 활용).
3. **베이스라인 및 예측 모델 구성:** `DummyClassifier(strategy='most_frequent')`를 베이스라인 모델로 설정하고, `StandardScaler`와 `LogisticRegression(max_iter=1000)`을 결합한 `Pipeline`을 메인 후보 모델로 구축합니다.
4. **임계값(Threshold) 최적화 및 예외 처리:** Validation 세트에서 임계값 후보 `[0.35, 0.50, 0.65]`에 따른 $F_2$ 점수를 비교하여 가장 높은 값을 선택합니다. 동점 발생 시 **더 높은 임계값**을 우선 선택합니다. 단, 특정 분할에서 타겟 클래스가 단일 클래스로만 구성되어 학습 또는 $F_2$ 계산이 불가능한 경우, 해당 사유를 명시하고 프로세스를 중단합니다.
5. **독립 테스트 세트 평가:** 최적화된 임계값을 Test 세트에 적용하여 정밀도(`Precision`), 재현율(`Recall`), $F_2$ 점수, 그리고 혼동 행렬(`Confusion Matrix`)을 산출합니다. Test 결과에 기반하여 임계값을 재조정하는 행위는 엄격히 금지됩니다.
6. **운영 데이터 추론 및 우선순위 선정:** 신규 운영 데이터(`incoming_claims.csv`)에 동일한 모델과 최적 임계값을 적용합니다. 임계값 이상인 접수를 대상으로 날짜별 **예측 점수 내림차순, 동점 시 `claim_id` 오름차순**으로 정렬한 뒤, 하루 최대 3건까지 검토 목록에 등록하고 나머지는 `NOT_SELECTED`로 처리합니다.
7. **평가 결과 리포팅 분리:** 최종 보고서에 **모델 임계값 기준의 Test 성능 지표**와 **일일 3건 제한이 적용된 실제 운영 선택 결과**를 명확히 구분하여 서술하며, 두 평가 기준의 지표를 혼동하여 기술하지 않습니다.

#### 입력 및 출력

**입력 파일:**
- `historical_claims.csv`: 과거 수리 접수 이력 (학습 및 검증용)
- `incoming_claims.csv`: 신규 운영 접수 데이터 (타겟 변수 및 사후 정보 제외)

**출력 파일:**
- **`evaluation.json`**: 데이터 분할별 고유 제품 수 및 샘플 수, 베이스라인 성능, 최적 선정 임계값(Threshold), 그리고 독립 Test 세트 평가 지표를 기록한 JSON 파일
- **`daily_review_queue.csv`**: `received_date,rank,claim_id,failure_score` — 검토 대상으로 최종 선정된 접수 건에 한해 날짜별, 순위 오름차순(`rank` 1~3)으로 정렬된 운영 검토 큐 파일
- **`incoming_decisions.csv`**: `claim_id,decision` — 모든 신규 운영 접수 건에 대한 판정 결과 (`SELECTED` 또는 `NOT_SELECTED`), 원본 입력 순서 및 행 개수 유지
- **`report.md`**: Feature 선택 사유, 정보 유출(Data Leakage) 및 그룹 분할 점검 내역, 일일 3건 제한 등의 운영 제약 사항, 그리고 주요 제한 사항을 서술한 마크다운 보고서

**예제 운영 점수** — Threshold가 `0.50`으로 결정된 경우

```csv
claim_id,received_date,failure_score
C04,2026-10-12,0.62
C02,2026-10-12,0.91
C03,2026-10-12,0.74
C01,2026-10-12,0.91
C05,2026-10-12,0.44
```

**예제 검토 목록**

```csv
received_date,rank,claim_id,failure_score
2026-10-12,1,C01,0.91
2026-10-12,2,C02,0.91
2026-10-12,3,C03,0.74
```

- `C01`, `C02`, `C03`, `C04`는 모두 임계값(`0.50`)을 상회하여 기준을 충족했습니다. 이 중 점수가 높은 상위 3건(`C01`, `C02`, `C03`)이 일일 최대 검토 한도에 따라 최종 선정되었습니다.
- `C04`: 임계값(`0.50`)은 통과하였으나, 일일 최대 검토 한도(3건) 제약으로 인해 최종 선택 목록에서 제외되었습니다.
- `C05`: 예측 점수(`0.44`)가 임계값 미달이므로 제외되었습니다.

#### 검증 항목 (Validation Criteria)

- **그룹 분할 무결성 검증:** 동일한 제품(`unit_id`)의 접수 기록이 Train, Validation, Test 등 서로 다른 평가 구간에 중복 분할되지 않고 완전히 격리되었는지 확인
- **정보 유출 차단 검증:** 사후 지표인 `confirmed_failure`와 `final_repair_cost`가 예측 Feature 세트에 일절 포함되지 않았는지 검증
- **임계값 및 운영 제약 정합성 검증:** 
  - Threshold 동점 발생 시 더 높은 임계값 선택 규칙 준수 여부
  - 예측 점수 동점 발생 시 `claim_id` 오름차순 정렬 규칙 준수 여부
  - Threshold 미달 건의 제외 처리 적정성
  - 일일 최대 3건의 검토 한도가 날짜별로 정확히 적용되는지 확인
- **운영 추론 독립성 검증:** 운영 검토 목록(`daily_review_queue.csv`) 및 판정 결과 생성 시 Test 타겟(Label) 정보를 일절 참조하거나 사용하지 않는지 확인
- **평가 및 운영 결과 분리 검증:** 모델 임계값 기준의 순수 Test 성능 지표와 3건의 일일 제한이 적용된 실제 운영 선택 결과가 혼동되지 않고 명확히 구분되어 산출되었는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 제품 단위 그룹 분할 및 데이터 정합성 검증**
   - `unit_id`를 기준으로 Train(60%)·Validation(20%)·Test(20%) 세트를 분할하고, 세 구간 간의 제품 ID 교집합이 완전히 비어 있는지(`empty`) 엄격히 검증합니다.
   - 허용된 입력 Feature(`age_months`, `alarm_count_30d`, `prior_claim_count`) 외의 사후 정보나 타겟 변수가 파이프라인에 유입되지 않도록 정합성을 검사합니다.
     ```python
     import pandas as pd
     from sklearn.model_selection import GroupShuffleSplit
   
     df = pd.read_csv("historical_claims.csv")
   
     # TODO: 필수 Feature 정수 범위 검사 및 유효하지 않은 레코드 분리
   
     # TODO: GroupShuffleSplit을 활용한 Train / Validation / Test 분할 및 제품 ID 교집합 검증
     ```

**STEP 2. 모델 학습, 임계값 최적화 및 운영 추론 수행**
   - 베이스라인 모델(`DummyClassifier`)과 `StandardScaler`, `LogisticRegression`을 결합한 `Pipeline`을 구성하여 학습을 진행합니다.
   - Validation 세트에서 임계값 후보 `[0.35, 0.50, 0.65]`에 따른 $F_2$ 점수를 평가하여 최적의 임계값를 선택합니다 (동점 시 더 높은 임계값 선택).
   - 확정된 임계값으로 Test 세트 성능을 측정(`evaluation.json`)하고, 신규 운영 데이터(`incoming_claims.csv`)에 적용하여 일일 최대 3건 제한 및 정렬 규칙에 맞는 운영 검토 큐를 생성합니다.
     ```python
     import json
     import pandas as pd
     from sklearn.dummy import DummyClassifier
     from sklearn.linear_model import LogisticRegression
     from sklearn.metrics import f2_score
     from sklearn.pipeline import Pipeline
     from sklearn.preprocessing import StandardScaler
   
     # TODO: DummyClassifier 및 StandardScaler + LogisticRegression Pipeline 정의 및 학습
   
     # TODO: Validation 세트에서 임계값 [0.35, 0.50, 0.65]별 F2 계산 및 최적 임계값 선정
   
     # TODO: Test 세트 평가 및 evaluation.json 저장
   
     # TODO: incoming_claims.csv 예측, 임계값 필터링, 일일 최대 3건 제한(점수 내림차순, claim_id 오름차순) 적용 후 CSV 출력
     ```
</details>

---

### P-02. Municipal Waste Demand Prediction — 시계열 분할과 잔차 분석을 활용한 지역별 주간 폐기물 수거량 수요 예측

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Regression · [Chapter 04](../Chapter-04/README.md) · Temporal Split · Baseline · Residual Analysis · Hyperparameter Selection

#### 문제 설명

지방자치단체는 효율적인 차량 배차와 인력 운용을 위해 각 행정 구역별 **다음 주 폐기물 수거량**을 정확히 예측하고자 합니다. 제공되는 데이터에는 과거 주차별 실제 수거량 이력뿐만 아니라, 다음 주에 예정된 지역 행사 수 및 환경 변수들이 포함되어 있습니다.

그러나 본 과제 설계 시 두 가지 핵심 과제를 해결해야 합니다.
첫째, 미래의 정보가 과거 학습 과정에 유출되지 않도록 시간 흐름을 엄격히 반영한 **시계열 분할(Temporal Split)** 을 적용해야 합니다.
둘째, 단순한 전체 평균 오차(RMSE/MAE) 축소에만 매몰될 경우, 수거량이 적은 구역과 많은 구역 간의 스케일 차이로 인해 특정 대규모 구역에서 반복적인 과대·과소 예측 오류가 발생하여 실제 배차 현장에 혼선이 빚어질 수 있습니다. 

본 과제에서는 과거 주차의 정보만을 활용하여 다음 주 수거량을 예측하는 회귀 모델을 구축하고, 구역별 예측 잔차(Residual) 분석을 통해 모델의 안정성과 실무 적합성을 함께 검증하시오.

#### 제공 데이터

분석 및 예측 모델 학습을 위해 단일 데이터셋 파일인 `weekly_waste.csv`가 제공되며, UTF-8 인코딩의 CSV 형식입니다. 각 행은 특정 구역(`zone_id`)과 주차(`forecast_week`)의 조합을 나타내며, 중복 없이 유일합니다. 데이터셋은 최소 15개 이상의 서로 다른 주차(`forecast_week`)에 걸친 시계열 이력을 포함합니다.

| 열 이름 | 의미 | 데이터 사용 가이드 / 제약 사항 |
| :--- | :--- | :--- |
| `zone_id` | 행정 구역 고유 식별자 | 구역별 특성 및 공간적 단위 파악용 |
| `forecast_week` | 예측 대상 주의 시작일 (월요일) | **시계열 분할(Temporal Split) 및 순서 정렬 기준** |
| `last_week_kg` | 직전 주 실제 수거량 (kg) | 시계열 래그(Lag) 특성으로 모델의 입력 Feature로 사용 가능 |
| `planned_events` | 예정된 행사 수 | 예측 대상 주에 계획된 행사 수 (예측 시점 사전 확정 값, Feature 사용 가능) |
| `holiday_days` | 공휴일 수 | 예측 대상 주의 공휴일 수 (사전 확인 가능 값, Feature 사용 가능) |
| `next_week_kg` | 다음 주 실제 수거량 (kg) | 모델 학습 및 평가를 위한 **타겟(Target) 전용** (0 이상의 유한한 실수) |

> ⚠️ **주의 사항:** 미래의 정보가 학습 과정에 유입되는 것을 방지하기 위해, 데이터 분할 시 무작위 분할이 아닌 `forecast_week` 기준의 **시간 순서형 분할(Temporal Split)** 을 엄격히 적용해야 합니다.

#### 요구사항

1. **데이터 정합성 및 무결성 검증:** 날짜 형식 유효성, 동일 구역·주차(`zone_id`, `forecast_week`) 조합의 중복 여부, 그리고 음수 수거량 등 비정상 입력 데이터를 검사하고 정제합니다.
2. **시계열 기반 데이터 분할 (Temporal Split):** 구역별 샘플을 무작위로 섞지 않고, 고유 주차(`forecast_week`)의 전체 개수($W$)를 기준으로 시간 순서에 따라 Train 60%(`floor(0.6W)`), Validation 20%(`floor(0.2W)`), Test(나머지 20%) 비율로 엄격히 분할합니다. 세 구간 간 주차가 중복되어서는 안 됩니다.
3. **Feature 및 Target 정의:** 직전 주 수거량(`last_week_kg`), 예정 행사 수(`planned_events`), 공휴일 수(`holiday_days`)를 모델의 입력 Feature로 사용합니다. `zone_id`는 구역별 성능 분석 및 그룹화에만 활용하며 모델의 직접적인 입력 Feature로는 제외합니다. `next_week_kg`는 타겟(Target)으로 설정합니다.
4. **베이스라인 및 회귀 모델 구성:** 직전 주 수거량을 그대로 예측하는 방식(`last_week_kg` Persistence)을 베이스라인 모델로 설정합니다. 후보 모델로는 `StandardScaler`와 `Ridge` 회귀 모델을 결합한 파이프라인을 구축하며, 규제 강도(`alpha`) 후보군은 `[0.1, 1.0, 10.0]`으로 설정합니다.
5. **하이퍼파라미터 최적화 및 비교 평가:** Validation 세트에서 MAE(Mean Absolute Error)가 가장 낮은 `alpha`를 최적 파라미터로 선택합니다 (동점 시 더 작은 `alpha` 우선 선택). 베이스라인은 모델 선택 과정에 개입하지 않으며, 최종 Test 세트에서 베이스라인과 Ridge 모델의 MAE 및 RMSE 성능을 비교 평가합니다.
6. **구역별 잔차 분석 및 과소 예측 추출:** `zone_id`별 Test MAE 및 잔차(Residual) 평균을 산출합니다. 특히 실제 수거량이 예측값보다 큰 **과소 예측 사례** 중 `actual - predicted` 편차가 가장 큰 상위 5건을 별도로 식별하고 기록합니다.
7. **결과 리포팅 및 운영 영향 분석:** 전체 지표와 구역별 세부 성능 간의 괴리가 발생하는 이유를 분석하고, 폐기물 수거량 과소 예측이 실제 현장 배차 및 인력 운영에 미치는 운영적 리스크와 시사점을 보고서에 기술합니다.

#### 입력 및 출력

**입력:** `weekly_waste.csv`

**출력:**

- `test_predictions.csv`: `zone_id,forecast_week,actual,predicted,baseline,residual`
- `zone_metrics.csv`: `zone_id,sample_count,mae,mean_residual`
- `underprediction_top5.csv`: `zone_id,forecast_week,actual,predicted,residual`
- `report.md`: 분할 방법, 선택한 모델, Baseline 비교, 구역별 오류 분석

**예제 데이터 일부**

```csv
zone_id,forecast_week,last_week_kg,planned_events,holiday_days,next_week_kg
Z01,2026-06-01,420,2,0,455
Z02,2026-06-01,310,0,0,300
Z01,2026-06-08,455,1,0,448
```

Baseline은 각 행에서 `[420, 310, 455]`를 예측합니다. 이 세 행은 형식 확인용이며, 제시된 일부 데이터만으로 Train·Validation·Test를 구성하지 않습니다.

#### 검증 항목 (Validation Criteria)

- **시계열 주차 분할 무결성 검증:** 고유 주차(`forecast_week`)를 기준으로 순차 분할을 수행할 때, 동일 주차 내의 여러 구역 데이터가 서로 다른 평가 구간(Train·Validation·Test)으로 무작위 분산되지 않고 주차 단위로 온전히 격리되었는지 확인
- **정보 유출 차단 검증:** 타겟 변수(`next_week_kg`) 및 예측 시점에 사전에 확정되지 않은 미래의 정보가 입력 Feature 세트에 일절 포함되지 않았는지 검증
- **분할 및 튜닝 독립성 검증:** 주차별 데이터를 무작위로 섞어 분할하지 않았으며, 독립 Test 세트의 결과를 바탕으로 하이퍼파라미터(`alpha`)를 재조정하거나 모델을 수정하지 않았는지 확인
- **잔차 부호 정합성 검증:** `actual - predicted` 연산 시 잔차의 부호 규칙을 올바르게 적용하여 과소 예측(Under-prediction)과 과대 예측(Over-prediction)을 정확하게 판별 및 분리하는지 확인
- **구역별 편차 및 오차 트레이드오프 분석:** 전체 평균 지표(MAE)가 개선되었음에도 불구하고 특정 구역에서 대규모 오차가 발생하는 원인을 분석하고, 지역별 특성에 따른 모델의 일반화 성능 편차를 타당하게 설명하는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 데이터 정합성 검증 및 시계열 기반 주차 분할 (Temporal Split)**
   - 누락값, 음수 수거량, 비정상 날짜 형식 등 무결성 저해 요소를 검사하고 정제하며, 동일한 행정 구역(`zone_id`)과 주차(`forecast_week`) 조합의 중복 여부를 엄격히 검증합니다.
   - 미래 정보 유출(Data Leakage)을 원천 차단하기 위해 무작위 분할을 배제하고, 전체 고유 주차($W$)의 시간 순서를 기준으로 Train(60%)·Validation(20%)·Test(나머지 20%) 구간을 주차 단위로 온전히 격리하여 분할합니다.
   
   ```python
   import numpy as np
   import pandas as pd
   
   # 데이터 로드
   df = pd.read_csv("weekly_waste.csv")
   
   # TODO: 날짜 형식 유효성 검사, 중복 레코드 제거 및 음수 수거량 정제
   
   # TODO: 고유 forecast_week 기준 시간 순서형 Temporal Split 구현 (Train 60%, Val 20%, Test 20%)
   ```

**STEP 2. Ridge 모델 학습, 하이퍼파라미터 튜닝 및 구역별 잔차 분석**
   - `zone_id`를 직접적인 입력 피처에서 제외하고, 허용된 피처(`last_week_kg`, `planned_events`, `holiday_days`)와 타겟(`next_week_kg`)을 정의합니다. `StandardScaler`와 `Ridge`(`alpha` 후보: `[0.1, 1.0, 10.0]`)를 결합한 파이프라인을 구축하여 Validation 세트의 MAE 기준으로 최적의 `alpha`를 선정합니다.
   - 독립된 Test 세트에서 베이스라인(`last_week_kg` Persistence)과 최적 Ridge 모델의 성능(MAE, RMSE)을 비교 평가하고, 구역별 잔차 분석을 통해 과소 예측(`actual - predicted`) 상위 5건을 추출한 뒤 최종 결과 파일 및 보고서를 생성합니다.
   
   ```python
   from sklearn.compose import ColumnTransformer
   from sklearn.linear_model import Ridge
   from sklearn.metrics import mean_absolute_error, mean_squared_error
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   
   features = ["last_week_kg", "planned_events", "holiday_days"]
   target = "next_week_kg"
   
   # TODO: Validation 세트를 활용한 최적 alpha(0.1, 1.0, 10.0) 튜닝 및 Ridge 파이프라인 학습
   
   # TODO: Test 세트에 대한 Baseline(직전 주 수거량) 및 최적 Ridge 모델 예측 수행
   
   # TODO: 구역별(zone_id) MAE 및 잔차 산출, 과소 예측 상위 5건 식별 후 결과 파일 및 리포트 저장
   ```

</details>

---

### P-03. 공유 오피스 공간 이용 패턴 군집화 및 안정성 검증

#### 문제 배경 및 개요

공유 오피스 운영사는 공간별 예약률과 취소율 데이터를 바탕으로 이용 패턴을 세분화하여 운영 효율성을 극대화하고자 합니다. 현재 사전에 정의된 공간 유형 레이블(Label)이 부재한 상태이므로, 비지도 학습(Unsupervised Learning)을 통한 데이터 주도형 공간 군집화가 요구됩니다.

그러나 단순한 클러스터링 결과 도출만으로는 실무적인 의사결정으로 이어지기 어렵습니다. 운영팀이 즉각적인 공간 운영 전략을 수립하기 위해서는 **각 군집의 정성적·정량적 특성(Cluster Profile)을 명확히 해석**할 수 있어야 하며, 알고리즘 초기화(Initialization) 변화에 따른 **군집 결과의 안정성(Reliability)과 신뢰도**가 뒷받침되어야 합니다.

본 과제에서는 KMeans 알고리즘을 활용해 공간 이용 패턴을 군집화하고, 군집별 프로파일링 분석 및 평가 신뢰도 검증을 거쳐 실무에 즉시 적용 가능한 공간 운영 최적화 전략을 도출합니다.

#### 제공 데이터

`workspace_usage.csv`: `room_id,week_start,weekly_bookings,avg_session_min,evening_ratio,cancel_ratio`

각 행은 특정 공간의 주차별 이용 기록입니다. 비율 관련 열은 0에서 1 사이의 값을 가지며, 주간 예약 수와 평균 이용 시간은 0 이상의 실수입니다. `room_id`와 `week_start`의 조합은 중복 없이 유일하며, 데이터셋은 최소 50개 이상의 유효 레코드를 포함합니다.

#### 요구사항

1. **데이터 정합성 및 무결성 검증:** 음수, 허용 범위를 벗어난 비율 값, 결측값, 그리고 동일 공간·주차(`room_id`, `week_start`) 조합의 중복 여부를 검사하고 정제하며, 제외된 행에 대한 사유를 명시합니다.
2. **Feature 표준화:** `weekly_bookings`, `avg_session_min`, `evening_ratio`, `cancel_ratio`를 추출하여 `StandardScaler`를 통해 평균 0, 분산 1의 스케일로 정규화합니다.
3. **KMeans 군집화 반복 실행:** `n_clusters=3`, `n_init=10`으로 설정된 `KMeans` 모델을 `random_state` 각각 `[7, 21, 42]`에서 순차적으로 실행합니다.
4. **군집 안정성(ARI) 검증:** 동일한 유효 샘플 순서를 기준으로, 서로 다른 `random_state` 실행 결과 간의 Adjusted Rand Index(ARI)를 계산하여 군집 할당의 안정성을 평가합니다. (단, 클러스터 번호 자체는 임의로 부여되므로 순수 매핑 결과로만 비교)
5. **기준 클러스터 프로파일링:** `random_state=42`를 기준 모델로 설정하고, 각 군집별 샘플 수, 원본 단위 Feature 평균 값, 그리고 공간별(room_id) 배정 분포를 산출합니다.
6. **운영 전략 도출 및 한계 분석:** 프로파일링 결과를 바탕으로 구체적인 공간 운영 변경안 3가지를 제안합니다. 각 제안에는 관찰된 클러스터 특징, 제안 근거, 적용 후 성과 측정 지표가 포함되어야 하며, 초기화 조건에 따른 안정성 한계가 있을 경우 이를 함께 보고합니다.

#### 입력 및 출력

**입력:** `workspace_usage.csv`

**출력:**

- `cluster_assignments.csv`: `room_id,week_start,cluster_id` (기준 결과)
- `cluster_profiles.csv`: `cluster_id,sample_count,mean_weekly_bookings,mean_avg_session_min,mean_evening_ratio,mean_cancel_ratio`
- `stability.csv`: `seed_a,seed_b,ari` (7–21, 7–42, 21–42 순서)
- `report.md`: 세 가지 운영 변경안과 검증 지표

**예제 데이터 일부**

```csv
room_id,week_start,weekly_bookings,avg_session_min,evening_ratio,cancel_ratio
M01,2026-09-07,18,55,0.62,0.05
M02,2026-09-07,6,160,0.14,0.10
M01,2026-09-14,20,48,0.70,0.08
```

출력 Cluster ID와 ARI 값은 전체 데이터에 따라 달라지므로 고정된 정답 숫자를 요구하지 않습니다.

#### 검증 항목

* **ARI 연산 무결성 검증:** Adjusted Rand Index(ARI)를 동일한 유효 샘플 순서를 기준으로 서로 다른 `random_state` 간의 클러스터 할당 결과에 올바르게 적용하여 산출했는지 확인
* **라벨 순서 독립성 검증:** 클러스터 번호(ID)가 임의로 스위칭되더라도 ARI가 두 할당 결과 간의 구조적 일치도를 올바르게 측정하는지 확인
* **평가 지표 적절성 검증:** 정답 레이블(Label)이 존재하지 않는 비지도 학습 문제에서 부적절한 지도 학습 지표(예: Accuracy) 대신 군집화 평가 지표를 올바르게 채택했는지 확인
* **운영 제안 타당성 검증:** 도출된 운영 변경안이 각 클러스터의 정량적 프로파일 및 실제 이용 특징과 논리적으로 긴밀하게 연결되어 있는지 확인
* **패널 데이터 특성 반영 검증:** 동일 공간(`room_id`)에 대한 시계열·반복 기록의 존재를 인식하고, 공간별 배정 분포 및 패턴 해석 시 이를 적절히 고려했는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 데이터 무결성 검증, 스케일링 및 KMeans 군집 안정성(ARI) 검증**
   - 허용 범위를 벗어난 값, 결측값, 중복 행을 엄격히 검사·정제하고, 분석 대상 Feature(`weekly_bookings`, `avg_session_min`, `evening_ratio`, `cancel_ratio`)를 `StandardScaler`로 표준화합니다.
   - `KMeans(n_clusters=3, n_init=10)` 모델을 `random_state` `[7, 21, 42]` 조건에서 각각 수행하고, 동일한 유효 샘플 순서를 기준으로 실행 결과 간 Adjusted Rand Index(ARI)를 계산하여 초기화에 따른 군집 할당의 안정성을 평가합니다.
   
   ```python
   import numpy as np
   import pandas as pd
   from sklearn.cluster import KMeans
   from sklearn.metrics import adjusted_rand_score
   from sklearn.preprocessing import StandardScaler
   
   # 데이터 로드
   df = pd.read_csv("workspace_usage.csv")
   
   # TODO: 범위 오류, 결측값, 중복 행 검사 및 정제 (제외 사유 기록)
   
   # TODO: StandardScaler를 활용한 Feature 정규화 수행
   
   # TODO: random_state [7, 21, 42]에 따른 KMeans 실행 및 ARI 기반 군집 안정성 검증
   ```

**STEP 2. 기준 클러스터 프로파일링 및 공유 오피스 운영 전략 도출**
   - `random_state=42`를 기준 모델로 선정하여 각 클러스터별 샘플 수, 원본 단위 Feature 평균 값, 그리고 공간별(`room_id`) 배정 분포를 산출하여 정성적·정량적 특성(Cluster Profile)을 해석합니다.
   - 프로파일링 결과를 바탕으로 관찰된 특징, 제안 이유, 성과 측정 지표가 포함된 구체적인 공간 운영 변경안 3가지를 도출하고, 초기화 조건에 따른 군집 안정성의 한계를 함께 보고합니다.
   
   ```python
   # TODO: random_state=42 기준 클러스터 프로파일링 (샘플 수, 원본 단위 Feature 평균, 공간별 배정 분포 산출)
   
   # TODO: 클러스터별 특성 분석 및 3가지 운영 변경안 작성 (한계 보고 포함)
   ```

</details>

---

## Challenge

### C-01. 제조 설비 고장 예측 시스템 감사 및 데이터 누수 검증 (Equipment Failure Model Audit)

#### 문제 배경 및 개요

제조 시설의 설비 고장 예측 모델이 내부 검증 단계에서는 우수한 성능을 기록했으나, 신규 설비 도입 시 실제 고장 탐지율이 급감하는 치명적인 문제가 발생했습니다.

개발 로그 분석 결과, 동일 설비(`equipment_id`)의 시계열 측정 기록이 Train과 Test 세트에 무작위로 분산(Data Splitting Leakage)되어 있었으며, 입력 Feature에 **고장 발생 이후에 기록되어야 하는 '수리 처리 코드(Post-failure Maintenance Code)'** 와 같은 미래 정보가 포함된 심각한 데이터 누수(Data Leakage) 정황이 포착되었습니다.

본 과제에서는 기존 모델의 과대평가(Overestimation) 원인을 코드 수준에서 재현 및 분석하고, 그룹 구조를 반영한 올바른 교차 검증(`GroupKFold`) 체계와 정합성이 확보된 Feature 파이프라인을 구축하여 모델의 진정한 일반화 성능을 복구하는 것을 목표로 합니다.

#### 제공 데이터

`equipment_history.csv`: 제조 설비의 센서 측정 이력 및 고장 여부가 포함된 단일 데이터셋 파일입니다. 동일한 설비(`device_id`)에 대한 다수의 시계열 측정 기록이 존재하며, 데이터셋은 최소 30대 이상의 서로 다른 설비 이력을 포함합니다. 일부 레코드에는 결측값이나 유효하지 않은 Feature 값이 포함되어 있을 수 있습니다.

| 열 이름 | 의미 | 데이터 사용 가이드 / 제약 사항 |
| :--- | :--- | :--- |
| `record_id` | 측정 레코드 고유 번호 | 결과 매핑 및 레코드 식별용 |
| `device_id` | 설비 고유 식별자 | **Group 교차 검증 분할 기준 (GroupKFold)** |
| `observed_at` | 측정 시각 | 시계열 흐름 및 기록 시점 정합성 점검용 |
| `temperature_c` | 측정 시점의 온도 (°C) | 모델 입력 Feature |
| `vibration_rms` | 측정 시점의 진동값 (RMS) | 모델 입력 Feature |
| `load_pct` | 측정 시점의 부하율 (0~100) | 모델 입력 Feature |
| `days_since_service` | 마지막 정비 이후 경과일 | 모델 입력 Feature |
| `failure_next_14d` | 측정 시점 이후 14일 이내 고장 여부 (0/1) | **머신러닝 모델 학습 및 평가 타겟 (Target)** |
| `final_repair_code` | 고장 확인 후 기록되는 수리 코드 | ⚠️ **사용 금지 (사후 정보 유출 Feature 원천 차단 대상)** |

#### 요구사항

1. **기존 과대평가 재현 및 문제 진단:** 전체 데이터를 무작위로 분할한 취약한 베이스라인 파이프라인을 구축하여 과대평가된 성능을 측정하고, 동일 설비(`device_id`)가 Train·Test 세트에 동시에 포함되는지(Data Splitting Leakage) 구조적으로 확인합니다.
2. **Feature 감사 및 누수 원천 차단:** 각 열의 데이터 생성 및 획득 시점을 엄격히 검토하여, 사후 정보인 `final_repair_code` 및 타겟 관련 변수가 입력 Feature 세트에 포함되지 않도록 차단합니다. 모델 학습에 허용된 정상 Feature 목록을 코드에 명시적으로 정의합니다.
3. **그룹 기반 교차 분할(Group-Based Split):** 무작위 분할을 배제하고 고유 설비(`device_id`)를 기준으로 Train 60%, Validation 20%, Test 20% 비율의 그룹 분할을 수행하여, 동일 설비의 기록이 여러 구간에 겹치지 않고 온전히 격리되도록 보장합니다.
4. **누수 없는 파이프라인(Leakage-Free Pipeline) 구축:** 결측값 처리(Training 세트 기준 중앙값 대치), `StandardScaler`, 그리고 `Logistic Regression`을 결합한 파이프라인을 구축합니다. 스케일러와 임퓨터를 포함한 모든 전처리 파라미터의 `fit()`은 반드시 해당 Training 구간 내에서만 수행되어야 합니다.
5. **다각도 모델 평가 및 비교:** Majority Baseline과 오류가 복구된 로지스틱 회귀 모델의 Accuracy, Recall, Balanced Accuracy, F1 Score를 비교 평가합니다. 특정 평가 구간에 실제 양성 클래스가 부재할 경우의 예외 처리 원칙 및 보고 방식을 명시합니다.
6. **성능 격차 원인 분석 및 리포팅:** 무작위 분할과 그룹 분할 간의 성능 차이, Feature Leakage의 영향, 그리고 설비별 오류 분포를 정량·정성적 근거로 분석하여 실제 현장 도입 관점에서 어떤 평가 체계가 타당한지 서술합니다. (단, 성능 하락 폭에 대한 인위적인 가정은 배제)
7. **회귀 테스트(Regression Test) 구현:** 파이프라인의 무결성을 자동으로 검증하는 테스트 코드를 작성합니다. 
   - (a) Train·Validation·Test 간 설비 ID(`device_id`) 교집합이 완전히 비어 있는지 확인
   - (b) 금지된 Feature가 모델 학습 입력에 포함되지 않았는지 확인
   - (c) Training 구간 외부에서 전처리(`fit`)가 누출되지 않았는지 검증
   - (d) 동일 `random_state` 설정 시 데이터 분할 결과가 완벽히 재현되는지 확인

#### 입력 및 출력

**입력:** `equipment_history.csv`

**출력:**

- `data_audit.csv`: `record_id,error_code` — 처리 불가능한 행과 오류 이유
- `split_audit.json`: 행 단위 분할의 Group 중복 수, 복구 분할의 Group 교집합 수, Sample·Group 수
- `metric_comparison.csv`: `evaluation,model,accuracy,recall,balanced_accuracy,f1`
- `error_by_device.csv`: `device_id,sample_count,false_negative_count,false_positive_count` (복구된 Test 대상)
- `root_cause_report.md`: 원인, 수정 근거, 남아 있는 한계, 테스트 결과

**점검용 예시**

```text
Train device_id = {D01, D02, D03}
Test  device_id = {D03, D04}
```

위 분할의 `D03`은 양쪽에 존재합니다. **새 설비 평가를 위한 Group 분할은 해당 교집합이 빈 집합이 되어야 합니다.** 점검용 예시는 실제 CSV의 전체 데이터가 아닙니다.

#### 검증 항목

* **Feature 허용 범위 및 사후 누수 차단 검증:** 모델 학습 시 허용된 Feature만 명시적으로 선택되었으며, 성능 확인 이후에도 금지된 열(`final_repair_code` 등)이 재유입되지 않았는지 확인
* **데이터 무결성 및 정제 일관성 검증:** 비정상적·유효하지 않은 입력값이 모델 학습에 포함되는지 여부를 점검하고, 결측치 및 이상치 처리 기준이 파이프라인 전체에 일관되게 적용되었는지 확인
* **분할 방식에 따른 성능 격차 비교 검증:** 행 단위 무작위 분할과 설비 기준(`device_id`) 그룹 분할의 결과를 명확히 구분하여 보고하고, 각 방식이 모델 성능에 미친 영향을 논리적으로 분석했는지 확인
* **평가 절차 독립성 및 과적합 방지 검증:** 독립된 Test 세트의 결과를 바탕으로 분할 조건이나 하이퍼파라미터를 반복적으로 수정하여 과적합을 유도하지 않았는지 확인
* **과대평가 원인 규명 및 일반화 타당성 검증:** 수정 전 취약한 파이프라인에서 나타난 과도하게 높은 성능이 왜 신규 설비 환경에서 실제 성능을 입증하는 근거가 될 수 없는지 구조적·논리적으로 설명했는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

**STEP 1. 피처 감사(Feature Audit) 및 사후 정보 유출 차단**
   - 데이터셋의 전체 열 목록과 각 변수의 생성 시점을 면밀히 검토하여, 설비 고장 예측 시점 이후에 만들어지거나 수집되는 사후 정보(예: `final_repair_code` 등)를 철저히 식별하고 입력 Feature 세트에서 원천 배제합니다.
   - 변수명이 숫자로 인코딩되어 있더라도 시점상 미래의 정보라면 학습에 포함되지 않도록 허용된 Feature 목록을 엄격히 정의합니다.

**STEP 2. 그룹 기반 분할(Group-Based Split) 및 누수 없는 파이프라인(Pipeline) 구축**
   - `GroupShuffleSplit` 등을 활용하여 고유 설비(`device_id`) 기준으로 데이터를 분할하고, 각 단계에서 Train·Validation·Test 세트 간의 설비 ID 교집합이 완벽히 공백인지(Data Leakage 방지) 검사합니다.
   - `SimpleImputer`, `StandardScaler`, `LogisticRegression`을 하나의 `Pipeline`으로 결합하여, 결측치 대치 및 스케일링 등의 전처리가 오직 Training 데이터 구간 내에서만 학습(fit)되도록 파이프라인의 무결성을 보장합니다.

**STEP 3. 모델 평가 절차 복구 및 성능 변화 분석**
   - 단순한 알고리즘 성능 개선과 평가 설계의 구조적 복구를 명확히 구분하여 기록합니다.
   - 수정 후 점수가 하락하더라도, 이것이 취약한 과대평가에서 벗어나 실제 신규 설비 환경을 신뢰성 있게 대변하는 올바른 평가 체계로의 전환임을 논리적으로 분석하고 리포팅합니다.

</details>

---

### C-02. 도서관 방문객 예측 시스템 복구 및 피처 정합성 검증 (Library Demand Forecast Recovery)

#### 문제 배경 및 개요

도서관 방문객 예측 모델은 일일 운영 인력 배치를 최적화하기 위해 과거 방문 기록을 활용합니다. 그러나 최근 데이터 제공 시스템이 개편된 이후, 특정 날짜에서 예측값이 비정상적으로 폭발하거나 데이터 파싱 단계에서 프로세스가 중단되는 치명적인 오류가 발생했습니다.

원인 조사 결과, ① 온도 측정 단위의 변경(기존 섭씨 `temperature_c`에서 화씨 `temperature_f`로의 변동), ② 필수 필드의 누락(결측값), ③ 동일 일자에 대한 중복 레코드 유입 등 데이터 정합성(Feature Consistency)을 훼손하는 요인들이 복합적으로 작용했음이 확인되었습니다.

본 과제에서는 추정이나 임의의 보간(Imputation)으로 유효하지 않은 입력을 억지로 메우는 비정상적 처리를 배제하고, 데이터 포맷 및 단위 변화를 엄격히 감지하여 정합성이 확보된 유효 행만을 선별·반영하는 강건한(Robust) 회귀 예측 파이프라인 및 시간 순서 기반 평가 체계를 복구합니다.

#### 제공 데이터

- `history_v1.csv`: 모델 학습용 과거 이력 데이터셋 (최소 120일 이상의 일자별 기록 포함, 날짜(`date`)는 중복 없이 유일함)
  - 주요 열: `date`(날짜), `temperature_c`(섭씨 온도), `scheduled_events`(예정 행사 수), `is_weekend`(주말 여부), `visitors_next_day`(익일 방문객 수 - **Target**)
- `incoming_v2.csv`: 실시간 예측 대상 데이터셋 (업무 시작 전 확보된 기상 예보 온도 및 행사 정보 포함)
  - 주요 열: `date`(날짜), `temperature_f`(화씨 온도), `scheduled_events`(예정 행사 수), `is_weekend`(주말 여부)

#### 요구사항

1. **입력 버전별 명시적 스키마 정의:** `history_v1`은 섭씨 온도(`temperature_c`), `incoming_v2`는 화씨 온도(`temperature_f`) 스키마를 각각 고유하게 적용하며, 정의되지 않은 열 이름을 임의로 추측하거나 자동 대체하지 않습니다.
2. **온도 단위 변환 및 유효성 검증:** 화씨 온도는 공식 $C = (F - 32) \times 5/9$를 적용하여 섭씨로 변환합니다. `temperature_f`는 유한한 실수여야 하며, 결측값 발생 시 필수 Feature 누락으로 판정합니다.
3. **도메인 제약 조건 및 예외 처리:** `scheduled_events`는 0 이상의 정수, `is_weekend`는 0 또는 1의 바이너리 값이어야 합니다. 필수 필드 누락 또는 허용 범위를 벗어난 비정상 행은 예측 대상에서 배제하고, 오류 코드와 함께 `rejected_rows.csv`에 기록합니다.
4. **날짜 중복 정합성 정책:** 동일 날짜(`date`)의 입력 데이터가 중복 유입될 경우, 최초의 유효 행만 정상 채택합니다. 무효 행은 날짜 슬롯을 점유하지 않으며, 이후 유효한 중복 행은 `DUPLICATE_DATE` 코드로 거부합니다.
5. **시계열 분할 및 모델 검증 체계:** 과거 히스토리 데이터를 시간 순서대로 Train 60%, Validation 20%, Test 나머지 비율로 분할합니다. Training Target 평균을 Baseline으로 설정하고, `StandardScaler`와 `Ridge(alpha=1.0)` 파이프라인의 후보 모델 성능(MAE)을 Validation 세트로 비교·선택하되, Test 결과로 모델을 재선택하지 않습니다.
6. **안전성 기반 추론 파이프라인:** 검증 단계를 통과한 최종 모델에만 신규 인입 데이터를 투입하며, 예측 수행 가능 행과 거부된 행을 엄격히 분리하여 출력합니다.
7. **예측 결과 포맷팅:** 정상 입력에 대해 예측 날짜, 변환된 섭씨 온도, 예상 방문객 수(실수 유지 및 파일 저장 시 소수점 둘째 자리 포맷팅)를 정확히 출력합니다.
8. **종합 리포트 작성 (`recovery_report.md`):** 데이터 오류 원인 분석, 정상 행 처리 현황, 과거 Test 성능 결과, 신규 인입 데이터의 거부 건수 및 복구 검증 결과를 포함한 종합 감사 리포트를 작성합니다.

#### 입력 및 출력

**입력:** `history_v1.csv`, `incoming_v2.csv`

**출력:**

- `normalized_incoming.csv`: `date,temperature_c,scheduled_events,is_weekend` (유효하고 중복 없는 행, 입력 순서)
- `rejected_rows.csv`: `source_line,error_code` (헤더 포함 실제 파일 행 번호)
- `predictions.csv`: `date,predicted_visitors` (정상 행의 원본 순서)
- `recovery_report.md`: 수정 내용과 검증 결과

**예제 입력** (`incoming_v2.csv`)

```csv
date,temperature_f,scheduled_events,is_weekend
2026-10-01,77,1,0
2026-10-02,,0,0
2026-10-01,80,1,0
2026-10-03,68,0,1
```

**예제 정규화 결과** (`normalized_incoming.csv`)

```csv
date,temperature_c,scheduled_events,is_weekend
2026-10-01,25.0000,1,0
2026-10-03,20.0000,0,1
```

**예제 거부 결과** (`rejected_rows.csv`)

```csv
source_line,error_code
3,MISSING_TEMPERATURE
4,DUPLICATE_DATE
```

이 예제는 입력 검증용입니다. `predictions.csv`의 예상 방문객 수는 학습된 모델에 따라 달라지므로 여기서는 고정하지 않습니다.

#### 검증 항목

* **온도 단위 변환 정밀도 검증:** 화씨-섭씨 변환 공식(예: $77^\circ\text{F} \to 25^\circ\text{C}$, $68^\circ\text{F} \to 20^\circ\text{C}$)이 수치 오차 없이 정확히 적용되었는지 확인
* **날짜 중복 점유 정책 검증:** 비정상(무효) 행이 선행 유입되었더라도 날짜 슬롯을 먼저 점유하지 않으며, 최초의 유효 행만 정상 채택되고 후속 유효 행이 `DUPLICATE_DATE`로 올바르게 거부되는지 확인
* **무허가 대치 및 보간 차단 검증:** 결측값이나 범위 이탈 등 무효 행을 임의의 값(예: 0, 평균값 등)으로 조용히 대치하거나 변조하지 않고 엄격하게 거부 처분하는지 확인
* **Feature 의미론적 일관성 검증:** 온도 단위 변환(섭씨/화씨) 전후에 걸쳐 Feature가 도메인 관점에서 동일한 물리적 의미와 척도를 일관되게 유지하는지 확인
* **평가 단계와 인입 예측의 분리 검증:** 과거 히스토리 기반의 Test 세트 성능 평가와 신규 인입 데이터에 대한 실시간 예측 결과를 혼동하지 않고 명확히 구분하여 다루는지 확인
* **출력 보호 및 원자적 갱신 검증:** 복구 및 검증 과정 실패 시 기존의 신뢰할 수 있는 정상 예측 결과 파일을 무분별하게 덮어쓰거나 유실시키지 않도록 안전하게 보호하는지 확인

**STEP 1. 스키마 버전 감지, 정규화 및 행 번호 추적 설계**
   - 입력 파일 읽기 단계에서 명시적인 스키마 버전(`history_v1`과 `incoming_v2`)을 안전하게 구분하고, 온도 단위를 비롯한 변수들을 공통 Feature 구조로 정규화합니다.
   - 원본 데이터의 행 번호(Row Index)를 철저히 보존하여, 유효성 검증 과정에서 발생하는 이상치나 오류 항목의 위치를 `rejected_rows.csv` 상에서 정확히 추적할 수 있도록 설계합니다.

**STEP 2. 엄격한 유효성 검사, 단위 변환 및 중복 날짜 정합성 관리**
   - 화씨 온도를 섭씨 공식($C = (F - 32) \times 5/9$)으로 정밀하게 변환하고, 0 이상의 행사 수 및 주말 바이너리 값 등 도메인 제약 조건을 검증하여 무효 행을 임의 대치 없이 엄격하게 거부합니다.
   - 동일 날짜 중복 입력 시 최초의 유효 행만 정상 채택하며, 무효 행이 날짜 슬롯을 먼저 점유하지 않도록 차단하고 후속 유효 중복 행은 `DUPLICATE_DATE` 코드로 처리합니다.

**STEP 3. 시계열 모델 검증 체계 구축 및 안전성 기반 실시간 추론**
   - 기존 히스토리 데이터를 시간 순서대로 분할하여 Baseline과 Ridge 회귀 모델의 검증(Validation 및 Test) 성능 평가 절차를 완결한 뒤, 검증을 통과한 최종 모델만 신규 인입 데이터 추론에 투입합니다.
   - 정답 Target이 존재하지 않는 신규 입력에 대해 예측 가능 행과 거부된 행을 명확히 분리 출력하고, 최종 예측 결과 포맷팅(소수점 둘째 자리) 및 종합 감사 리포트(`recovery_report.md`)를 작성합니다.

---

## Radiant

### R-01. The City That Never Sleeps — 도시 공공시설 통합 운영 분석

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · AI Application & Limitations · [Chapter 02](../Chapter-02/README.md) · Regression · Feature Engineering · Leakage · [Chapter 03](../Chapter-03/README.md) · Classification · Clustering · [Chapter 04](../Chapter-04/README.md) · Evaluation Protocol · Imbalanced Metrics · Group·Temporal Split · Pipeline

#### 문제 설명

한 도시의 여러 공공시설은 방문객 수, 전력 사용량, 설비 경보를 매일 기록하고 있습니다. 운영 부서는 다음 날의 시설 이용 규모를 예측하고, 가까운 시일 내 고장 위험이 높은 시설을 찾아 점검 순서를 결정하려고 합니다. 시설별 이용 패턴을 구분해 운영 계획에 참고하는 기능도 필요합니다.

기존 분석 시스템에서는 문제가 반복되고 있습니다. 같은 날짜의 기록이 중복 전송되고, 일부 시설은 다른 시설과 데이터의 범위가 크게 다릅니다. 미래에 확인된 고장 여부가 학습 Feature에 섞인 코드도 발견되었습니다. 이전 담당자는 전체 Accuracy가 높다는 이유로 모델을 배포했지만, 실제 고장을 놓친 사례가 여러 건 발생했습니다.

문제는 **공공시설 운영을 위한 분석 시스템을 신뢰할 수 있는 상태로 재설계하는 것** 입니다. 단순히 모델 세 개를 학습하는 것으로 끝나지 않습니다. 데이터 검증, 적절한 평가, 운영 제약, 오류 처리, 결과 재현성과 처리 효율까지 하나의 프로그램으로 연결해야 합니다.

#### 제공 데이터와 시점

모든 데이터는 실습용 합성 데이터입니다. 실제 시설 운영 기록이나 개인 정보는 포함하지 않습니다.

**1. `facilities.csv` — 시설 기준 정보**

```csv
facility_id,district,capacity
F01,NORTH,300
F02,SOUTH,180
```

- `facility_id`: 시설의 고유 ID
- `district`: 지역명(집계·운영 규칙에 사용)
- `capacity`: 시설의 수용 인원, 1 이상의 정수

**2. `daily_operations.csv` — 과거 관측값과 사후 확정 Target**

```csv
facility_id,date,visitors,energy_kwh,temperature_c,alarms_7d,failure_next_7d,visitors_next_day,final_repair_cost
F01,2026-04-01,120,50,21,1,0,126,0
F01,2026-04-02,126,52,22,0,0,119,0
```

| 열 | 의미 | 사용 기준 |
|---|---|---|
| `facility_id`, `date` | 시설·관측 날짜 | 데이터 연결, 시점 구분 |
| `visitors` | 해당 날짜에 관측한 방문객 수 | Feature |
| `energy_kwh` | 해당 날짜의 전력 사용량 | Feature |
| `temperature_c` | 해당 날짜의 기온 | Feature |
| `alarms_7d` | 해당 날짜까지 최근 7일의 경보 건수 | Feature |
| `failure_next_7d` | 해당 날짜 **이후 7일 안에** 고장이 발생했는지 여부 | Classification Target |
| `visitors_next_day` | 해당 날짜 다음 날의 방문객 수 | Regression Target |
| `final_repair_cost` | 고장 처리 후 확정된 수리 비용 | **Feature 사용 금지** |

**3. `incoming_operations.csv` — 운영용 최신 관측값**

```csv
facility_id,date,visitors,energy_kwh,temperature_c,alarms_7d
F01,2026-07-01,130,53,23,1
F02,2026-07-01,82,34,23,0
```

최신 관측값에는 정답 Target이 없으며, 그날의 관측이 끝난 뒤 다음 날 수요와 향후 7일의 고장 위험을 예측합니다.

#### 데이터 처리 규칙

1. 세 파일은 헤더가 있는 UTF-8 CSV입니다. `facility_id`와 `date`의 조합은 `daily_operations.csv`에서 유일해야 하며, `incoming_operations.csv`에서도 유일해야 합니다.
2. `facilities.csv`의 `facility_id`는 중복되면 안 됩니다. 시설 기준 정보에 중복 또는 필수 열 누락이 있으면 전체 처리를 중단하고 원인을 출력합니다.
3. `daily_operations.csv`와 `incoming_operations.csv`에서는 **첫 번째 유효한 시설·날짜 기록만 인정** 합니다. 무효 행은 해당 키를 점유하지 않으며, 이후 발견된 유효 중복 행은 `DUPLICATE_RECORD`로 거부합니다.
4. 등록되지 않은 시설은 `UNKNOWN_FACILITY`, 유한하지 않은 수 또는 음수 방문객·전력·경보 수는 `INVALID_NUMBER`, 과거 Target의 형식이나 범위가 잘못된 경우는 `INVALID_TARGET`으로 기록합니다.
5. `failure_next_7d`는 0 또는 1이고, `visitors_next_day`는 0 이상의 정수입니다. `visitors`, `alarms_7d`도 0 이상의 정수입니다. `energy_kwh`는 0 이상의 유한 실수입니다. `temperature_c`는 유한 실수이며 음수도 허용합니다.
6. `final_repair_cost`는 이 과제에서 사용하지 않는 사후 기록입니다. 입력 파일에 존재하더라도 학습 Feature 또는 평가 기준으로 이용하지 않습니다.
7. 무효 행을 제외한 뒤 `facility_id`, `date`의 고유성이 유지되어야 합니다. 오류 행은 `source_file,source_line,error_code` 순으로 기록하며, `source_line`은 헤더를 포함한 실제 파일 행 번호입니다.

#### 구현 요구사항

**STEP 01 — 데이터 검증과 추적 가능성**

- 입력 파일의 Schema, 필수 열, 숫자 범위, 시설 ID의 존재 여부를 확인합니다.
- 유효한 기록과 오류 기록을 분리하고, 데이터 건수·시설 수·오류 코드별 건수를 기록합니다.
- 정상 데이터를 정렬한 파일을 생성합니다. 정렬 기준은 **날짜 오름차순, 같은 날짜에서는 시설 ID 오름차순** 입니다.
- 거부된 행은 이후 모델 학습·예측에 영향을 주어서는 안 됩니다.

**STEP 02 — 미래 정보가 섞이지 않는 평가 분할**

과거 데이터는 다음 기간으로 구분합니다.

| 구간 | 기록 날짜 | 사용 목적 |
|---|---|---|
| Training | 2026-01-01 ~ 2026-04-30 | 모델·전처리 기준 학습 |
| Gap 1 | 2026-05-01 ~ 2026-05-07 | 평가에서 제외 |
| Validation | 2026-05-08 ~ 2026-05-31 | Threshold·모델 후보 선택 |
| Gap 2 | 2026-06-01 ~ 2026-06-07 | 평가에서 제외 |
| Test | 2026-06-08 ~ 2026-06-30 | 최종 성능 확인 |

고장 Target이 미래 7일을 대상으로 하므로 구간 사이에 7일의 Gap을 둡니다. Gap의 기록은 학습·설정 선택·최종 점수에 포함하지 않습니다. 제공된 데이터는 최소 10개 시설과 각 평가 구간의 유효 기록을 포함한다고 가정합니다.

또한 새로운 시설에 대한 일반화 여부도 따로 확인합니다.

- 고유한 `facility_id`를 문자열 오름차순으로 정렬합니다.
- **5번째, 10번째, 15번째 … 시설** 을 신규 시설 평가용 Holdout으로 정합니다. 이 시설의 모든 기록은 Training·Validation 및 전처리 학습에서 제외합니다.
- **평가 A:** Holdout이 아닌 기존 시설의 Test 기간 성능
- **평가 B:** 학습에 전혀 사용하지 않은 Holdout 시설의 Test 기간 성능

두 평가 결과는 따로 보고합니다. Holdout 시설의 Target을 이용해 모델이나 Threshold를 선택하지 않습니다. Holdout이 아닌 시설의 Training과 Validation에서만 설정을 선택합니다.

**STEP 03 — 설비 고장 위험 Classification**

- 허용된 숫자형 Feature는 `visitors`, `energy_kwh`, `temperature_c`, `alarms_7d`, `capacity`입니다.
- Baseline으로 `DummyClassifier(strategy='most_frequent')`를 사용합니다.
- 후보 모델은 `StandardScaler`와 `LogisticRegression(max_iter=1000)`을 연결한 Pipeline입니다.
- Validation에서 Threshold `[0.25, 0.40, 0.55]`의 F2를 비교합니다. 동점일 경우 큰 Threshold를 선택합니다.
- 확정한 모델과 Threshold를 사용해 평가 A·B에서 Precision·Recall·F2·Confusion Matrix를 구합니다. 평가 구간에 실제 양성이 없거나 양성 예측이 없을 때는 분모가 0인 지표를 구분하여 보고합니다.
- 운영용 입력에서는 Threshold를 통과한 시설을 **지역·날짜별 최대 10개** 까지 점검 대상으로 등록합니다. 점수 내림차순, 동점이면 시설 ID 오름차순으로 선택합니다. 선택하지 않은 시설도 점수와 미선택 이유를 보존합니다.

**STEP 04 — 다음 날 방문객 수 Regression**

- 같은 Feature에서 Target을 `visitors_next_day`로 바꿉니다.
- Baseline은 각 시설의 **해당 날짜 `visitors`를 다음 날 값으로 그대로 예측** 하는 방법입니다.
- 후보 모델은 `StandardScaler` + `Ridge`이며 `alpha` 후보 `[0.1, 1.0, 10.0]`을 Validation MAE로 비교합니다. 동점이면 작은 `alpha`를 선택합니다.
- 평가 A·B에서 MAE·RMSE를 계산합니다. 지역별 MAE와 과소 예측이 큰 사례도 별도로 기록합니다.
- 최종 선택한 회귀 모델을 운영용 입력에 적용합니다.

**STEP 05 — 시설 이용 패턴 Clustering**

- Training 기간의 Holdout이 아닌 시설 기록에서 `visitors`, `energy_kwh`, `alarms_7d`만 사용합니다.
- Training Data로 StandardScaler를 학습하고 `KMeans(n_clusters=3, n_init=10, random_state=42)`를 적용합니다.
- Cluster별 Sample 수와 **원본 단위** 의 Feature 평균을 계산합니다.
- 기준 결과의 안정성을 확인하기 위해 동일한 Training Data에서 `random_state=7` 결과와 ARI를 계산합니다.
- 운영용 데이터의 Cluster를 지정할 때는 이미 학습한 Scaler와 KMeans의 `predict()`를 사용합니다. 운영 데이터로 중심을 다시 학습하지 않습니다.
- Cluster ID를 시설의 확정된 등급이나 정답 Label로 해석하지 않습니다.

**STEP 06 — 결과 재현성 및 장애 대응**

- 동일 입력, 동일 라이브러리 환경, 동일 Parameter에서 반복 실행했을 때 결과 행 순서와 파일 내용이 일치해야 합니다.
- 필수 입력 파일을 읽지 못하면 이전 정상 결과 파일을 덮어쓰지 않습니다.
- 유효한 데이터가 부족하거나 학습 구간의 Classification Target이 한 클래스뿐이라 모델을 학습할 수 없다면, 임의의 점수를 생성하지 않고 이유를 보고합니다.
- 결과 파일은 먼저 별도 임시 디렉터리에 모두 생성·검사한 뒤 배포합니다. 여러 파일을 한 번에 교체하는 작업은 원자적이지 않으므로 부분 실패를 탐지하고 이전 결과로 복구하는 방법을 문서화합니다.
- 운영 입력에는 실제 Target이 없으므로 운영용 데이터에 대한 MAE나 Recall을 계산하지 않습니다.

**STEP 07 — 처리 효율 분석**

- 올바른 기준 구현을 완성한 뒤 같은 Schema의 **100,000행 이상 실습용 합성 데이터** 로 처리 시간과 메모리 사용량을 측정합니다.
- 행마다 전체 시설 목록을 반복 탐색하는 방법과 Dictionary 조회·Pandas 결합 등을 이용한 방법을 비교할 수 있습니다.
- 최적화 전후에 데이터 검증 결과와 출력 행이 동일한지 확인해야 합니다.
- 처리 시간, 데이터 규모, 측정 환경과 개선 근거를 기록합니다. 빠른 실행을 위해 검증이나 평가를 생략해서는 안 됩니다.

#### 입력 및 출력 규격

**입력:** `facilities.csv`, `daily_operations.csv`, `incoming_operations.csv`

**출력:**

| 파일 | 포함할 내용 |
|---|---|
| `clean_history.csv` | 허용된 과거 행, 날짜·시설 ID 오름차순 |
| `rejected_rows.csv` | `source_file,source_line,error_code` |
| `split_report.json` | 구간별 Sample·시설 수, Gap 제외 수, 신규 시설 Holdout ID, Group 교집합 확인 |
| `model_report.json` | 모델·Threshold·Alpha 선택 결과, Baseline, 평가 A·B의 지표 |
| `test_predictions.csv` | 시설 ID, 날짜, 고장 실제값·점수·예측, 방문객 실제값·예측값·Residual, 평가 A/B |
| `operational_predictions.csv` | 시설 ID, 날짜, 고장 점수, 다음 날 방문객 예측, Cluster ID |
| `inspection_queue.csv` | 날짜, 지역, 점검 순위, 시설 ID, 고장 점수 |
| `cluster_profiles.csv` | Cluster ID, Sample 수, 원본 단위 평균 |
| `performance_report.md` | 데이터 규모, 처리 시간, 메모리 사용량, 비교 결과 |
| `final_report.md` | 설계 근거, 장애 원인, 복구 정책, 평가·오류 분석, 남아 있는 한계 |

숫자형 점수는 파일에서 소수 넷째 자리까지, 예측 방문객 수는 소수 둘째 자리까지 기록합니다. 파일 내부 정렬 규칙을 일관되게 적용합니다. 출력 폴더에 기존 결과가 있다면 복구 가능한 상태로 보존해야 합니다.

#### 공개 검증 예제 — 행 검증과 중복 제어

다음 입력은 **STEP 01 검증용** 입니다. 전체 모델 학습을 수행하기 위한 크기의 데이터는 아닙니다.

**예제 입력** (`daily_operations.csv`)

```csv
facility_id,date,visitors,energy_kwh,temperature_c,alarms_7d,failure_next_7d,visitors_next_day,final_repair_cost
F01,2026-04-01,120,50,21,1,0,126,0
F01,2026-04-01,130,51,22,1,0,129,0
F02,2026-04-01,-5,30,19,0,1,45,0
F02,2026-04-01,55,30,19,0,0,60,0
```

`facilities.csv`에는 `F01`, `F02`가 유효하게 등록되어 있다고 가정합니다.

**예제 출력** (`rejected_rows.csv`)

```csv
source_file,source_line,error_code
daily_operations.csv,3,DUPLICATE_RECORD
daily_operations.csv,4,INVALID_NUMBER
```

**정상 기록 결과** (`clean_history.csv`에 포함되는 데이터 행)

```csv
F01,2026-04-01,120,50,21,1,0,126,0
F02,2026-04-01,55,30,19,0,0,60,0
```

첫 번째 `F01` 기록만 인정합니다. `F02`의 무효 행은 키를 점유하지 않으므로 그다음 유효 기록은 정상 처리합니다.

#### 최종 검증 항목

1. **데이터 무결성:** 입력 오류와 중복이 예측 결과에 반영되지 않는지 확인
2. **정보 누출 방지:** 사후 Target·수리비, 미래 날짜, 평가용 Holdout 데이터가 학습 Feature나 설정 선택에 사용되지 않는지 확인
3. **독립적인 평가:** 기존 시설과 신규 시설의 성능을 별도로 계산하고 Test에서 재조정하지 않는지 확인
4. **운영 규칙:** 지역별 일일 점검 한도, 동점 처리, Threshold 미달 및 정렬 규칙이 지켜지는지 확인
5. **Clustering 해석:** Cluster ID가 임의의 번호이고, 결과의 안정성과 실제 특징을 분석했는지 확인
6. **복구 가능성:** 실패한 실행이 이전의 정상 결과를 손상하지 않고, 오류 이유가 추적 가능한지 확인
7. **재현성:** 같은 입력에 대한 파일 내용과 순서가 반복 실행에서 일치하는지 확인
8. **성능 개선:** 처리 시간이 줄어도 분석 결과가 바뀌지 않는지 검증

#### 제출 결과물

실행 코드, 요구되는 출력 파일, 자동 테스트, 실행 명령과 의존 라이브러리를 기록한 문서, 최종 분석 보고서를 제출합니다. 코드 구조는 자유롭게 설계할 수 있지만, **예측 결과를 재현하고 오류가 발생한 이유를 설명할 수 있어야 합니다.**

<details>
<summary><strong>구현 가이드</strong></summary>

1. **입력 계약부터 고정:** CSV별 필수 열과 오류 코드를 정의하세요. 정상 행만 모아 모델 단계에 전달하면 학습 코드가 단순해집니다.
2. **분할과 Feature 목록부터 검증:** 모델을 만들기 전에 날짜 구간, Holdout 시설 목록, 허용 Feature 목록을 먼저 검사하세요.
3. **Baseline과 첫 모델 구현:** Classification·Regression의 기준 성능을 기록한 다음 후보 모델을 추가하세요. 설정 선택은 Validation에서 끝내야 합니다.
4. **분석 과제 분리:** Classification과 Regression은 Label이 필요하지만 Clustering은 Label 없이 패턴을 찾습니다. 세 결과가 서로 다른 목적을 가진다는 점을 유지하세요.
5. **운영 규칙과 평가 분리:** Test의 성능 지표와 운영 점검 대상 선정은 서로 다른 출력입니다. 후자는 용량 제한까지 반영해야 합니다.
6. **오류·재현성 테스트:** 누락 열, 비정상 숫자, 중복 키, 미래 Target 혼입, 한 클래스만 있는 데이터, 결과 파일 교체 실패를 각각 검증하세요.
7. **최적화는 마지막에:** 기준 구현과 결과가 동일하다는 것을 먼저 확인한 뒤 처리 시간을 비교하세요.

</details>

---

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)
